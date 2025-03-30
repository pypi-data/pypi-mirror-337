from __future__ import annotations

from asyncio import Event, create_task, sleep, wait_for
from base64 import b64encode, urlsafe_b64encode
from collections import defaultdict
from json import loads
from logging import getLogger
from random import getrandbits
from traceback import print_exception
from typing import TYPE_CHECKING
from uuid import uuid4
from xml.etree.ElementTree import XMLPullParser

from aiohttp import ClientSession, WSMsgType

from .errors import WSConnectionError, XMPPClosed, XMPPException
from .utils import utc_now

if TYPE_CHECKING:
    from asyncio import Task
    from collections.abc import Callable, Iterable
    from datetime import datetime
    from typing import Any
    from xml.etree.ElementTree import Element

    from aiohttp import ClientWebSocketResponse, WSMessage

    from ._types import Dict, Listener, ListenerDeco, NCo
    from .auth import AuthSession
    from .http import XMPPConfig


if __import__("sys").version_info <= (3, 11):
    from asyncio import TimeoutError


__all__ = (
    "Context",
    "EventDispatcher",
    "Stanza",
    "XMLNamespaces",
    "XMLGenerator",
    "XMLProcessor",
    "XMPPWebsocketClient",
)


_logger = getLogger(__name__)


def make_stanza_id() -> str:
    # Full credit: aioxmpp
    _id = getrandbits(120)
    _id = _id.to_bytes((_id.bit_length() + 7) // 8, "little")
    _id = urlsafe_b64encode(_id).rstrip(b"=").decode("ascii")
    return ":" + _id


def make_resource(platform: str, /) -> str:
    return f"V2:Fortnite:{platform}::{uuid4().hex.upper()}"


def match(xml: Element, ns: str, tag: str, /) -> bool:
    return xml.tag == f"{{{ns}}}{tag}"


class Context:
    __slots__ = ("auth_session", "body", "created_at")

    def __init__(self, auth_session: AuthSession, body: Dict, /) -> None:
        self.auth_session: AuthSession = auth_session
        self.body: Dict = body
        self.created_at: datetime = utc_now()


class EventDispatcher:
    event_listeners: dict[str, list[Listener]] = defaultdict(list)
    presence_listeners: list[Listener] = []
    tasks: list[Task] = []

    @classmethod
    def on_event(cls, auth_session: AuthSession, body: Dict, /) -> None:
        event = body.get("type")
        ctx = Context(auth_session, body)
        for func in cls.event_listeners.get(event, []):
            cls.run_coro(func(ctx))

    @classmethod
    def on_presence(cls, auth_session: AuthSession, body: Dict, /) -> None:
        ctx = Context(auth_session, body)
        for func in cls.presence_listeners:
            cls.run_coro(func(ctx))

    @classmethod
    def run_coro(cls, coro: NCo, /) -> None:
        task = create_task(coro)
        cls.tasks.append(task)
        task.add_done_callback(cls.on_task_complete)

    @classmethod
    def on_task_complete(cls, task: Task, /) -> None:
        try:
            cls.tasks.remove(task)
        except ValueError:
            pass

        exception = task.exception()
        if exception is not None:
            _logger.error("Dispatched event raised an exception")
            print_exception(exception)

    @classmethod
    def event(cls, event: str, /) -> ListenerDeco:
        def decorator(listener: Listener, /) -> Listener:
            cls.add_event_listener(event, listener)
            return listener

        return decorator

    @classmethod
    def presence(cls) -> ListenerDeco:
        def decorator(listener: Listener, /) -> Listener:
            cls.add_presence_listener(listener)
            return listener

        return decorator

    @classmethod
    def add_event_listener(cls, event: str, listener: Listener, /) -> None:
        cls.event_listeners[event].append(listener)
        _logger.debug(f"Added listener {listener} for event {event}")

    @classmethod
    def add_presence_listener(cls, listener: Listener, /) -> None:
        cls.presence_listeners.append(listener)
        _logger.debug(f"Added presence listener {listener}")

    @classmethod
    def remove_event_listener(cls, event: str, listener: Listener, /) -> None:
        try:
            cls.event_listeners[event].remove(listener)
        except ValueError:
            return
        _logger.debug(f"Removed listener {listener} for event {event}")

    @classmethod
    def remove_presence_listener(cls, listener: Listener, /) -> None:
        try:
            cls.presence_listeners.remove(listener)
        except ValueError:
            return
        _logger.debug(f"Removed presence listener {listener}")


class Stanza:
    __slots__ = ("name", "text", "children", "attributes")

    def __init__(
        self,
        *,
        name: str,
        text: str = "",
        children: Iterable[Stanza] = (),
        make_id: bool = True,
        **attributes: str,
    ) -> None:
        children = tuple(children)
        if text and children:
            raise ValueError("Invalid combination of Stanza arguments passed")

        self.name: str = name
        self.text: str = text
        self.children: tuple[Stanza, ...] = children
        self.attributes: dict[str, str] = attributes
        if make_id:
            self.attributes["id"] = make_stanza_id()

    def __str__(self) -> str:
        attrs_str = ""
        for key, value in self.attributes.items():
            key = key.strip("_")
            attrs_str += f" {key}='{value}'"
        if self.text:
            return f"<{self.name}{attrs_str}>{self.text}</{self.name}>"
        elif self.children:
            return f"<{self.name}{attrs_str}>{''.join(str(child) for child in self.children)}</{self.name}>"
        else:
            return f"<{self.name}{attrs_str}/>"

    def __eq__(self, other: Stanza | str, /) -> bool:
        return str(self) == str(other)

    @property
    def id(self) -> str | None:
        return self.attributes.get("id")


class XMLNamespaces:
    SESSION = "urn:ietf:params:xml:ns:xmpp-session"
    CLIENT = "jabber:client"
    STREAM = "http://etherx.jabber.org/streams"
    SASL = "urn:ietf:params:xml:ns:xmpp-sasl"
    BIND = "urn:ietf:params:xml:ns:xmpp-bind"
    PING = "urn:xmpp:ping"


class XMLGenerator:
    __slots__ = ("xmpp",)

    def __init__(self, xmpp: XMPPWebsocketClient, /) -> None:
        self.xmpp: XMPPWebsocketClient = xmpp

    @property
    def xml_prolog(self) -> str:
        return f"<?xml version='{self.xmpp.config.xml_version}'?>"

    @property
    def open(self) -> str:
        return (
            f"<stream:stream xmlns='{XMLNamespaces.CLIENT}' "
            f"xmlns:stream='{XMLNamespaces.STREAM}' "
            f"to='{self.xmpp.config.host}' "
            f"version='{self.xmpp.config.xmpp_version}'>"
        )

    @property
    def quit(self) -> str:
        return "</stream:stream>"

    @property
    def b64_plain(self) -> str:
        acc_id = self.xmpp.auth_session.account_id
        acc_tk = self.xmpp.auth_session.access_token
        return b64encode(f"\x00{acc_id}\x00{acc_tk}".encode()).decode()

    def make_iq(self, **kwargs: Any) -> Stanza:
        return Stanza(
            name="iq", to=self.xmpp.config.host, from_=self.xmpp.jid, **kwargs
        )

    def make_message(self, *, to: str, **kwargs: Any) -> Stanza:
        return Stanza(name="message", to=to, from_=self.xmpp.jid, **kwargs)

    def make_presence(self, **kwargs: Any) -> Stanza:
        return Stanza(name="presence", from_=self.xmpp.jid, **kwargs)

    def auth(self, mechanism: str, /) -> Stanza:
        if mechanism == "PLAIN":
            auth = self.b64_plain
        else:
            # Expected authorization mechanism is PLAIN
            # But implement other mechanisms here if needed
            raise NotImplementedError
        return Stanza(
            name="auth",
            text=auth,
            make_id=False,
            xmlns=XMLNamespaces.SASL,
            mechanism=mechanism,
        )

    def bind(self, resource: str, /) -> Stanza:
        child2 = Stanza(name="resource", text=resource, make_id=False)
        child1 = Stanza(
            name="bind",
            xmlns=XMLNamespaces.BIND,
            children=(child2,),
            make_id=False,
        )
        return self.make_iq(type="set", children=(child1,))

    def ping(self) -> Stanza:
        child = Stanza(name="ping", xmlns=XMLNamespaces.PING, make_id=False)
        return self.make_iq(type="get", children=(child,))

    def session(self) -> Stanza:
        child = Stanza(
            name="session", xmlns=XMLNamespaces.SESSION, make_id=False
        )
        return self.make_iq(type="set", children=(child,))


class XMLProcessor:
    __slots__ = (
        "xmpp",
        "parser",
        "outbound_ids",
        "xml_depth",
    )

    def __init__(self, xmpp: XMPPWebsocketClient, /) -> None:
        self.xmpp: XMPPWebsocketClient = xmpp
        self.reset()

    def setup(self) -> None:
        self.parser = XMLPullParser(("start", "end"))  # noqa

    def reset(self) -> None:
        self.parser: XMLPullParser | None = None  # noqa
        self.outbound_ids: list[str] = []  # noqa
        self.xml_depth: int = 0  # noqa

    async def process(self, message: WSMessage, /) -> None:
        if self.parser is None:
            raise RuntimeError("XML parser doesn't exist")

        self.parser.feed(message.data)
        for event, xml in self.parser.read_events():

            if event == "start":
                self.xml_depth += 1

            elif event == "end":
                self.xml_depth -= 1

                if self.xml_depth == 0:
                    raise XMPPClosed(xml, "Stream closed")

                elif self.xml_depth == 1:
                    await self.handle(xml)

    async def handle(self, xml: Element, /) -> None:
        xml_id = xml.get("id")
        known = False

        if xml_id in self.outbound_ids:
            self.outbound_ids.remove(xml_id)
            known = True

        if not self.xmpp.negotiated:
            await self.negotiate(xml)
        elif "message" in xml.tag:
            self.handle_event(xml)
        elif "presence" in xml.tag:
            self.handle_presence(xml)
        elif not known:
            self.xmpp.auth_session.action_logger(
                f"Unknown message: {xml_id}", level=_logger.warning
            )

    def handle_event(self, xml: Element, /) -> None:
        type_ = xml.get("type")

        if type_ is not None and type_ != "normal":
            return

        from_ = xml.get("from")

        if from_ != "xmpp-admin@prod.ol.epicgames.com":
            return

        for sub_xml in xml:
            if "body" in sub_xml.tag:
                body = loads(sub_xml.text)
                break
        else:
            return

        EventDispatcher.on_event(self.xmpp.auth_session, body)

    def handle_presence(self, xml: Element, /) -> None:
        type_ = xml.get("type")

        if type_ is None or type_ == "available":
            available = True
        elif type_ == "unavailable":
            available = False
        else:
            return

        from_ = xml.get("from")

        if from_ is None or "-" in from_:
            return

        split = from_.split("@")
        user_id = split[0]
        platform = split[1].split(":")[2]

        status = None
        show = None

        for sub_xml in xml:
            if "status" in sub_xml.tag:
                status = loads(sub_xml.text)
            elif "show" in sub_xml.tag:
                show = sub_xml.text

        if status is None:
            return

        body = {
            "user_id": user_id,
            "platform": platform,
            "available": available,
            "show": show,
            "status": status,
        }
        EventDispatcher.on_presence(self.xmpp.auth_session, body)

    async def negotiate(self, xml: Element, /) -> None:
        negotiation: dict[tuple, Callable] = {
            (
                XMLNamespaces.STREAM,
                "features",
                (
                    XMLNamespaces.SASL,
                    "mechanisms",
                    (XMLNamespaces.SASL, "mechanism", None),
                ),
            ): self.sasl,
            (
                XMLNamespaces.STREAM,
                "features",
                (XMLNamespaces.BIND, "bind", None),
            ): self.bind,
            (XMLNamespaces.SASL, "success", None): self.sasl_success,
            (
                XMLNamespaces.CLIENT,
                "iq",
                (
                    XMLNamespaces.BIND,
                    "bind",
                    (XMLNamespaces.BIND, "jid", None),
                ),
            ): self.bind_success,
        }

        def traverse(_xml: Element, _pattern: tuple, /) -> Element | None:
            ns, tag, subpattern = _pattern

            if not match(_xml, ns, tag):
                return None
            elif subpattern is None:
                return _xml

            child = _xml.find(f"{{{subpattern[0]}}}{subpattern[1]}")

            if child is None:
                return None

            return traverse(child, subpattern)

        for pattern, callback in negotiation.items():
            result = traverse(xml, pattern)
            if result is not None:
                await callback(result)
                return

        raise XMPPException(xml, "Unable to negotiate stream")

    async def sasl(self, xml: Element, /) -> None:
        mechanism = xml.text
        self.xmpp.auth_session.action_logger(
            f"Attempting {mechanism} authentication.."
        )
        await self.xmpp.send_auth(mechanism)

    async def bind(self, _: Element, /) -> None:
        resource = make_resource(self.xmpp.config.platform)
        await self.xmpp.send_bind(resource)

    async def sasl_success(self, _: Element, /) -> None:
        self.xmpp.authenticated = True
        self.xmpp.auth_session.action_logger("Authenticated")
        self.reset()
        self.setup()
        await self.xmpp.send_open()

    async def bind_success(self, xml: Element, /) -> None:
        jid = xml.text
        resource = jid.split("/")[1]
        self.xmpp.resource = resource
        self.xmpp.auth_session.action_logger(f"Bound to JID {jid}")


class XMPPWebsocketClient:
    __slots__ = (
        "auth_session",
        "config",
        "session",
        "ws",
        "processor",
        "generator",
        "recv_task",
        "ping_task",
        "setup_task",
        "negotiated_event",
        "cleanup_event",
        "exceptions",
        "_resource",
        "_authenticated",
    )

    def __init__(self, auth_session: AuthSession, /) -> None:
        self.auth_session: AuthSession = auth_session
        self.config: XMPPConfig = auth_session.client.xmpp_config

        self.session: ClientSession | None = None
        self.ws: ClientWebSocketResponse | None = None

        self.processor: XMLProcessor = XMLProcessor(self)
        self.generator: XMLGenerator = XMLGenerator(self)

        self.recv_task: Task | None = None
        self.ping_task: Task | None = None
        self.setup_task: Task | None = None

        self.negotiated_event: Event | None = None
        self.cleanup_event: Event | None = None

        self.exceptions: list[Exception] = []

        self._resource: str | None = None
        self._authenticated: bool = False

    @property
    def jid(self) -> str:
        if self.resource:
            return f"{self.auth_session.account_id}@{self.config.host}/{self.resource}"
        else:
            return f"{self.auth_session.account_id}@{self.config.host}"

    @property
    def bound(self) -> bool:
        return bool(self.resource)

    @property
    def running(self) -> bool:
        return self.ws is not None and not self.ws.closed

    @property
    def negotiated(self) -> bool:
        return self.bound and self.authenticated

    @property
    def resource(self) -> str | None:
        return self._resource

    @resource.setter
    def resource(self, value: str | None, /) -> None:
        self._resource = value
        if self.negotiated:
            self.negotiated_event.set()

    @property
    def authenticated(self) -> bool:
        return self._authenticated

    @authenticated.setter
    def authenticated(self, value: bool, /) -> None:
        self._authenticated = value
        if self.negotiated:
            self.negotiated_event.set()

    @property
    def most_recent_exception(self) -> Exception | None:
        try:
            return self.exceptions[-1]
        except IndexError:
            return None

    def send_open(self) -> NCo:
        return self.send(self.generator.open, with_xml_prolog=True)

    def send_auth(self, mechanism: str, /) -> NCo:
        return self.send(self.generator.auth(mechanism))

    def send_bind(self, resource: str, /) -> NCo:
        return self.send(self.generator.bind(resource))

    def send_ping(self) -> NCo:
        return self.send(self.generator.ping())

    def send_quit(self) -> NCo:
        return self.send(self.generator.quit)

    async def send(
        self, source: Stanza | str, /, *, with_xml_prolog: bool = False
    ) -> None:
        if not self.running:
            raise RuntimeError("XMPP client is not running!")
        if isinstance(source, Stanza):
            if source.id is not None:
                self.processor.outbound_ids.append(source.id)
            source = str(source)
        if with_xml_prolog is True:
            source = self.generator.xml_prolog + source

        await self.ws.send_str(source)
        self.auth_session.action_logger(f"SENT: {source}")

    async def ping_loop(self) -> None:
        while True:
            await sleep(self.config.ping_interval)
            await self.send_ping()

    async def recv_loop(self) -> None:
        self.auth_session.action_logger("Websocket receiver running")

        try:
            while True:
                message = await self.ws.receive()

                if message.type == WSMsgType.TEXT:
                    self.auth_session.action_logger(f"RECV: {message.data}")
                    await self.processor.process(message)

                else:
                    raise WSConnectionError(message)

        except Exception as exception:
            if isinstance(exception, XMPPClosed):
                txt = "Websocket received closing message"
                level = _logger.debug
                print_exc = False
            else:
                txt = "Websocket encountered a fatal error"
                level = _logger.error
                print_exc = True

            self.auth_session.action_logger(txt, level=level)
            self.exceptions.append(exception)

            if print_exc is True:
                print_exception(exception)

            create_task(self.cleanup())  # noqa

        finally:
            self.auth_session.action_logger("Websocket receiver stopped")

    async def start(self) -> None:
        if self.running is True:
            return

        client = self.auth_session.client
        config = self.config

        self.session = ClientSession(
            connector=client.connector,
            connector_owner=client.connector is None,
        )
        self.ws = await self.session.ws_connect(
            f"wss://{config.domain}:{config.port}",
            timeout=config.connect_timeout,
            protocols=("xmpp",),
        )
        self.processor.setup()

        self.recv_task = create_task(self.recv_loop())
        self.ping_task = create_task(self.ping_loop())
        self.setup_task = create_task(self.setup())

        self.negotiated_event = Event()
        self.cleanup_event = Event()

        self.auth_session.action_logger("XMPP started")

        # Let one iteration of the event loop pass
        # Before sending our opening message
        # So the receiver can initialise first
        await sleep(0)
        await self.send_open()

    async def stop(self) -> None:
        if self.running is False:
            return

        await self.send_quit()

        try:
            event = self.wait_for_cleanup()
            timeout = self.config.stop_timeout
            await wait_for(event, timeout)

        except TimeoutError:
            await self.cleanup()

    async def setup(self) -> None:
        complete = False

        try:
            event = self.wait_for_negotiated()
            timeout = self.config.connect_timeout
            await wait_for(event, timeout)
            await self._setup()
            complete = True

        except (Exception, TimeoutError) as exception:
            txt, level = "Setup failed - aborting..", _logger.error

            self.auth_session.action_logger(txt, level=level)
            self.exceptions.append(exception)

            print_exception(exception)

            create_task(self.cleanup())  # noqa

        finally:
            if complete:
                self.auth_session.action_logger("Setup finished")
            else:
                self.auth_session.action_logger("Setup aborted")

    async def _setup(self) -> None:
        await self.send(self.generator.session())
        await self.send(self.generator.make_presence())
        # TODO: party setup
        ...

    async def wait_for_negotiated(self) -> None:
        try:
            await self.negotiated_event.wait()
        except AttributeError:
            raise RuntimeError("XMPP client is not running!")

    async def wait_for_cleanup(self) -> None:
        if self.cleanup_event is None:
            return
        await self.cleanup_event.wait()

    async def cleanup(self) -> None:
        for task in self.recv_task, self.ping_task, self.setup_task:
            if task and not task.done():
                task.cancel()

        for event in self.negotiated_event, self.cleanup_event:
            if event and not event.is_set():
                event.set()

        await self.ws.close()
        await self.session.close()

        self.session = None
        self.ws = None
        self.processor.reset()

        self.recv_task = None
        self.ping_task = None
        self.setup_task = None

        self.negotiated_event = None
        self.cleanup_event = None

        self.resource = None
        self.authenticated = False

        self.auth_session.action_logger("XMPP stopped")
