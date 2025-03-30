from typing import Dict, List, Tuple
import requests
import json
import os
import mimetypes
import time
from jarvis.jarvis_platform.base import BasePlatform
from jarvis.jarvis_utils.output import OutputType, PrettyOutput
from jarvis.jarvis_utils.utils import while_success
class KimiModel(BasePlatform):
    """Kimi model implementation"""

    platform_name = "kimi"

    def get_model_list(self) -> List[Tuple[str, str]]:
        """Get model list"""
        return [("kimi", "Based on the web Kimi, free interface")]

    def __init__(self):
        """
        Initialize Kimi model
        """
        super().__init__()
        self.chat_id = ""
        self.api_key = os.getenv("KIMI_API_KEY")
        if not self.api_key:
            message = (
                "需要设置 KIMI_API_KEY 才能使用 Jarvis。请按照以下步骤操作：\n"
                "1. 获取 Kimi API Key:\n"
                "   • 访问 Kimi AI 平台: https://kimi.moonshot.cn\n"
                "   • 登录您的账户\n"
                "   • 打开浏览器开发者工具 (F12 或右键 -> 检查)\n"
                "   • 切换到网络标签\n"
                "   • 发送任意消息\n"
                "   • 在请求中找到 Authorization 头\n"
                "   • 复制 token 值（去掉 'Bearer ' 前缀）\n"
                "2. 设置环境变量:\n"
                "   • 方法 1: 创建或编辑 ~/.jarvis/env 文件:\n"
                "   echo 'KIMI_API_KEY=your_key_here' > ~/.jarvis/env\n"
                "   • 方法 2: 直接设置环境变量:\n"
                "   export KIMI_API_KEY=your_key_here\n"
                "设置后，重新运行 Jarvis。"
            )
            PrettyOutput.print(message, OutputType.INFO)
            PrettyOutput.print("KIMI_API_KEY 未设置", OutputType.WARNING)
        self.auth_header = f"Bearer {self.api_key}"
        self.chat_id = ""
        self.first_chat = True  # 添加标记，用于判断是否是第一次对话
        self.system_message = ""

    def set_system_message(self, message: str):
        """Set system message"""
        self.system_message = message

    def set_model_name(self, model_name: str):
        """Set model name"""
        pass

    def _create_chat(self) -> bool:
        """Create a new chat session"""
        url = "https://kimi.moonshot.cn/api/chat"
        payload = json.dumps({
            "name": "Unnamed session",
            "is_example": False,
            "kimiplus_id": "kimi"
        })
        headers = {
            'Authorization': self.auth_header,
            'Content-Type': 'application/json'
        }
        try:
            response = while_success(lambda: requests.request("POST", url, headers=headers, data=payload), sleep_time=5)
            self.chat_id = response.json()["id"]
            return True
        except Exception as e:
            PrettyOutput.print(f"错误：创建会话失败：{e}", OutputType.ERROR)
            return False


    def chat(self, message: str) -> str:
        """Send message and get response"""
        if not self.chat_id:
            if not self._create_chat():
                raise Exception("Failed to create chat session")

        url = f"https://kimi.moonshot.cn/api/chat/{self.chat_id}/completion/stream"



        payload = {
            "messages": [{"role": "user", "content": message}],
            "use_search": True,
            "extend": {"sidebar": True},
            "kimiplus_id": "kimi",
            "use_research": False,
            "use_math": False,
            "refs": [],
            "refs_file": []
        }

        headers = {
            'Authorization': self.auth_header,
            'Content-Type': 'application/json'
        }

        try:
            response = while_success(lambda: requests.post(url, headers=headers, json=payload, stream=True), sleep_time=5)
            full_response = ""

            # 收集搜索和引用结果
            search_results = []
            ref_sources = []

            for line in response.iter_lines():
                if not line:
                    continue

                line = line.decode('utf-8')
                if not line.startswith("data: "):
                    continue

                try:
                    data = json.loads(line[6:])
                    event = data.get("event")

                    if event == "cmpl":
                        # 处理补全文本
                        text = data.get("text", "")
                        if text:
                            if not self.suppress_output:
                                PrettyOutput.print_stream(text)
                            full_response += text

                    elif event == "search_plus":
                        # 收集搜索结果
                        msg = data.get("msg", {})
                        if msg.get("type") == "get_res":
                            search_results.append({
                                "date": msg.get("date", ""),
                                "site_name": msg.get("site_name", ""),
                                "snippet": msg.get("snippet", ""),
                                "title": msg.get("title", ""),
                                "type": msg.get("type", ""),
                                "url": msg.get("url", "")
                            })

                    elif event == "ref_docs":
                        # 收集引用来源
                        ref_cards = data.get("ref_cards", [])
                        for card in ref_cards:
                            ref_sources.append({
                                "idx_s": card.get("idx_s", ""),
                                "idx_z": card.get("idx_z", ""),
                                "ref_id": card.get("ref_id", ""),
                                "url": card.get("url", ""),
                                "title": card.get("title", ""),
                                "abstract": card.get("abstract", ""),
                                "source": card.get("source_label", ""),
                                "rag_segments": card.get("rag_segments", []),
                                "origin": card.get("origin", {})
                            })

                except json.JSONDecodeError:
                    continue

            if not self.suppress_output:
                PrettyOutput.print_stream_end()


            # 显示搜索结果摘要
            if search_results and not self.suppress_output:
                output = ["搜索结果:"]
                for result in search_results:
                    output.append(f"- {result['title']}")
                    if result['date']:
                        output.append(f"  日期: {result['date']}")
                    output.append(f"  来源: {result['site_name']}")
                    if result['snippet']:
                        output.append(f"  摘要: {result['snippet']}")
                    output.append(f"  链接: {result['url']}")
                    output.append("")
                PrettyOutput.print("\n".join(output), OutputType.PROGRESS)

            # 显示引用来源
            if ref_sources and not self.suppress_output:
                output = ["引用来源:"]
                for source in ref_sources:
                    output.append(f"- [{source['ref_id']}] {source['title']} ({source['source']})")
                    output.append(f"  链接: {source['url']}")
                    if source['abstract']:
                        output.append(f"  摘要: {source['abstract']}")

                    # 显示相关段落
                    if source['rag_segments']:
                        output.append("  相关段落:")
                        for segment in source['rag_segments']:
                            text = segment.get('text', '').replace('\n', ' ').strip()
                            if text:
                                output.append(f"    - {text}")

                    # 显示原文引用
                    origin = source['origin']
                    if origin:
                        text = origin.get('text', '')
                        if text:
                            output.append(f"  原文: {text}")

                    output.append("")

                PrettyOutput.print("\n".join(output), OutputType.PROGRESS)

            return full_response

        except Exception as e:
            raise Exception(f"Chat failed: {str(e)}")

    def delete_chat(self) -> bool:
        """Delete current session"""
        if not self.chat_id:
            return True  # 如果没有会话ID，视为删除成功

        url = f"https://kimi.moonshot.cn/api/chat/{self.chat_id}"
        headers = {
            'Authorization': self.auth_header,
            'Content-Type': 'application/json'
        }

        try:
            response = while_success(lambda: requests.delete(url, headers=headers), sleep_time=5)
            if response.status_code == 200:
                self.chat_id = ""
                self.uploaded_files = []
                self.first_chat = True  # 重置first_chat标记
                return True
            else:
                PrettyOutput.print(f"删除会话失败: HTTP {response.status_code}", OutputType.WARNING)
                return False
        except Exception as e:
            PrettyOutput.print(f"删除会话时发生错误: {str(e)}", OutputType.ERROR)
            return False


    def name(self) -> str:
        """Model name"""
        return "kimi"
