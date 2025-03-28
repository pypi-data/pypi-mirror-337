from typing_extensions import Callable, List, Awaitable, Optional, override
import asyncio
import inspect
from nonebot import logger
from nonebot.exception import ProcessException, FinishedException, StopPropagation
from .event import SuggarEvent, FinalObject
from . import suggar
import sys
from nonebot.adapters.onebot.v11 import MessageSegment, MessageEvent, PokeNotifyEvent
from .exception import BlockException, PassException, CancelException

"""
suggar matcher
用于触发Suggar中间件事件
"""
event_handlers = {}
handler_infos = {}
matchers_data = {}
priority = {}


class SuggarMatcher:

    def __init__(self, event_type: str = ""):
        # 存储事件处理函数的字典
        global event_handlers, priority, handler_infos
        self.event_handlers = event_handlers
        self.handler_infos = handler_infos
        self.event_type = event_type
        self.event: SuggarEvent
        self.processing_message: MessageSegment
        self.priority = priority

    def handle(self, event_type=None, priority_value: int = 10, block=False):
        """
        事件处理函数注册函数
        参数：
          - event_type: 事件类型，默认为None，因为在on_event可能已经传入
          - priority_value: 事件优先级，默认为10
          - block: 是否阻塞事件，默认为False
        """
        if not priority_value > 0:
            raise ValueError("事件优先级不能为0或负！")
        if event_type == None and self.event_type != "":
            event_type = self.event_type
            if self.event_type == "" or self.event_type == None:
                raise ValueError("事件类型不能为空！")

        def decorator(func: Callable[[Optional[SuggarEvent]], Awaitable[None]]):
            global priority, handler_infos, event_handlers
            self.handler_infos = handler_infos
            self.priority = priority
            self.event_handlers = event_handlers
            if event_type not in self.event_handlers:
                self.event_handlers[event_type] = []
                self.handler_infos[event_type] = {}
                self.priority[event_type] = []
            self.event_handlers[event_type].append(func)
            if not priority_value in self.priority[event_type]:
                self.priority[event_type].append(priority_value)
            self.priority[event_type] = sorted(self.priority[event_type])
            self.handler_infos[event_type][id(func)] = {
                "func": func,
                "signature": inspect.signature(func),
                "frame": inspect.currentframe().f_back,
                "priority": priority_value,
                "block": block,
            }
            return func

        return decorator

    def stop_process(self):
        """
        阻止当前Suggar事件循环继续运行并立即停止当前的处理器。
        """
        raise BlockException()

    def cancel(self):
        """
        停止Nonebot层的处理器
        """
        raise FinishedException()

    def cancel_matcher(self):
        """
        停止当前Suggar事件处理并取消。
        """
        raise CancelException()

    def cancel_nonebot_process(self):
        """
        直接停止Nonebot的处理流程，不触发任何事件处理程序。
        """
        raise StopPropagation()

    def pass_event(self):
        """
        忽略当前处理器，继续处理下一个。
        """
        raise PassException()

    async def trigger_event(self, event: SuggarEvent, *args, **kwargs) -> SuggarEvent:
        """
        触发特定类型的事件，并调用该类型的所有注册事件处理程序。

        参数:
        - event: SuggarEvent 对象，包含事件相关数据。
        - **kwargs: 关键字参数，可能包含事件相关数据。
        - *args: 可变参数，可能包含事件相关数据。
        """
        event_type = self.event_type  # 获取事件类型
        self.event = event
        self.processing_message = event.message
        logger.info(f"开始为这个类型 {event_type} 的事件运行处理。")
        # 检查是否有处理该事件类型的处理程序
        if event_type in self.event_handlers:
            for priority in sorted(self.priority[event_type]):
                try:
                    logger.info(f"开始处理优先级为 {priority} 的 {event_type} 事件。")
                    # 遍历该事件类型的所有处理程序
                    for handler in self.event_handlers[event_type]:
                        info = self.handler_infos[event_type][id(handler)]
                        if info["priority"] != priority:
                            continue
                        # 获取处理程序的签名
                        sig = inspect.signature(handler)
                        line_number = info["frame"].f_lineno
                        file_name = info["frame"].f_code.co_filename

                        param_types = {
                            k: v.annotation for k, v in sig.parameters.items()
                        }
                        filtered_param_types = {
                            k: v
                            for k, v in param_types.items()
                            if v is not inspect._empty
                        }
                        # 创建一个新的参数列表
                        new_args = []
                        used_indices = set()
                        for param_name, param_type in filtered_param_types.items():
                            for i, arg in enumerate(args):
                                if i in used_indices:
                                    continue
                                if isinstance(arg, param_type):
                                    new_args.append(arg)
                                    used_indices.add(i)
                                    break
                        new_args_tuple = tuple(new_args)

                        # 获取关键词参数类型注解
                        params = sig.parameters
                        # 构建传递给处理程序的参数字典
                        f_kwargs = {}
                        for param_name, param in params.items():
                            if param.annotation in kwargs:
                                f_kwargs[param_name] = kwargs[param.annotation]
                        # 调用处理程序
                        try:
                            logger.info(
                                f"开始运行处理器： '{handler.__name__}'(~{file_name}:{line_number})"
                            )

                            await handler(event, *new_args_tuple, **f_kwargs)

                        except ProcessException as e:
                            logger.info("处理已停止。")
                            raise e
                        except PassException:
                            logger.info(
                                f"处理器 '{handler.__name__}'(~{file_name}:{line_number}) 已取消运行"
                            )
                            continue
                        except CancelException:
                            logger.info("事件处理已取消。")
                            return
                        except BlockException as e:
                            raise e
                        except Exception as e:
                            logger.error(
                                f"在运行处理器 '{handler.__name__}'(~{file_name}:{line_number}) 时遇到了问题"
                            )
                            exc_type, exc_value, exc_traceback = sys.exc_info()
                            logger.error(f"Exception type: {exc_type.__name__}")
                            logger.error(f"Exception message: {str(exc_value)}")
                            import traceback

                            back = ""
                            for i in traceback.format_tb(exc_traceback):
                                back += i
                            logger.error(back)
                            continue
                        finally:

                            logger.info(
                                f"'{handler.__name__}'(~{file_name}:{line_number}任务已结束。"
                            )
                            if info["block"]:
                                raise BlockException()
                except BlockException:
                    break
        else:
            logger.info(f"没有为这个事件: {event_type} 注册的处理器，跳过处理。")
        return FinalObject(self.processing_message)
