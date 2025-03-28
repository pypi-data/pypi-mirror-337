from openai import AzureOpenAI
from .whisper_db import WhisperDB
from .whisper_tools import WhisperTools_Qywx
import os
import json
from collections import defaultdict
import logging
logger = logging.getLogger("whisper_ai")

class AgentTrainer:
    def __init__(self):
        """ 初始化一个空字典用于存储函数 """
        self.assistant_id = "asst_7VzwDP4SBDltl3sEBB21baxx"
        self.task_list_done = []
        self.task_list = [
            "coach_get_selling_product",
            "coach_get_completed_order"
        ]
        self._error_count = 0

    def run(self, agent_list):
        #超过3次错误，就不再尝试！
        if self._error_count > 3:
            logger.error(f"错误次数超过3次，不再执行教练任务！！")
            return
        result = False
        for agent in agent_list:
            #logging.debug(f"{agent.get_kf_name()}准备执行教练任务！")
            for task_name in self.task_list:
                task = {
                    "task_name":task_name,
                    "kf_name":agent.get_kf_name()
                }
                if (task not in self.task_list_done):
                    #logging.debug(f"{agent.get_kf_name()}的{task_name}任务开始执行！")
                    agent.call(task_name, agent.get_kf_name())
                    self.task_list_done.append({"task_name":task_name, "kf_name":agent.get_kf_name()})
                    result = True
                    break
        if (not result):
            logger.info(f"所有任务已执行完成！")
        return result

    def clear_run(self):
        self.task_list_done = []
        self._error_count = 0
    def on_error(self, e):
        self._error_count = self._error_count + 1
        logger.error(f"AI教练出现异常，错误类型: {type(e).__name__}")
        logger.error(f"AI教练出现异常，错误信息: {e}")
        logger.error(f"AI教练出现异常，异常发生在: {e.__traceback__.tb_lineno} 行")
        WhisperTools_Qywx.send_to_error_robot(f"AI教练出现异常：({e}，{e.__traceback__.tb_lineno})")    

    def clear_error(self): 
        self._error_count = 0

    def daily_report(self, agent_kf): 
        # 设置OpenAI客户端
        client = AzureOpenAI(
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_version="2024-05-01-preview",
        )


        my_updated_assistant = client.beta.assistants.update(
            self.assistant_id,
            tool_resources={
                "file_search":{
                    "vector_store_ids": [agent_kf.get_vector_id()]
                }
            }
        )
        logger.info(my_updated_assistant)
        my_thread = client.beta.threads.create()

        result = self.get_yesterday_chat_list_shop(agent_kf)

        # 输出查询结果
        logger.info("chat_list:", result)

        # 如果查询结果存在
        if result:
            # 导出为 JSON 文件
            output_path = r"D:\WhisperAgent\信息收集\openai_chat_list.json"  # 替换为你想保存的路径
            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump(result, json_file, ensure_ascii=False, indent=4)

            logger.info(f"数据已成功导出到 {output_path}")
        else:
            logger.info("没有查询到数据")
            return

        file = client.files.create(
            file=open(output_path, "rb"),
            purpose="assistants"
        )
        logger.info("文件：", file)
        thread_message = client.beta.threads.messages.create(
            my_thread.id,
            role="user",
            content=[
                {
                    "type": "text",
                    "text": """这个文件是昨日的聊天记录，请根据聊天记录生成一份客服日报，日报中包含如下信息：
                            1、数据信息：包括接待的人数，售后几人、售前几人。
                            2、大家最关心的问题有哪些？（不超过3个）。
                            3、发现客户交流中最不满意的方面是什么？（不超过3个）
                            4、对客服知识库优化的建议。（不超过三点）
                            注意：如果附件中文件为空或者没有文件，则不用生成日报。
                        """,
                }
            ],
            attachments=[
                {
                    "file_id":file.id,
                    "tools":[
                        {"type":"code_interpreter"},
                        {"type":"file_search"}
                    ]
                }
            ]
        )
        logger.info(thread_message)

        run = client.beta.threads.runs.create_and_poll(
            thread_id=my_thread.id,
            assistant_id=self.assistant_id
        )

        if run.status == 'completed': 
            messages = client.beta.threads.messages.list(
                thread_id=my_thread.id,
                limit=1
            )
            logger.info(f"获取消息: {messages}")
            extracted_contents = []
            for message in messages.data:
                for content in message.content:
                    if content.type == "text":
                        text_value = content.text.value
                        #annotations = content.text.annotations  # 提取引用信息
                        
                        # 解析引用信息
                        #citations = []
                        #for annotation in annotations:
                        #    if hasattr(annotation, "file_citation"):  # 过滤文件引用
                        #        file_id = annotation.file_citation.file_id
                        #        ref_text = annotation.text  # 显示的引用文本
                        #        citations.append(f"{ref_text} -> 文件ID: {file_id}")
                        
                        # 组合文本和引用
                        formatted_text = text_value
                        #if citations:
                        #    formatted_text += "\n\n🔍 **引用信息:**\n" + "\n".join(citations)
                        
                        extracted_contents.append(formatted_text)

            # 返回完整的格式化信息
            #WhisperTools_Qywx.send_to_kf_robot(agent_kf, "\n\n---\n\n".join(extracted_contents))
            logger.info("\n\n---\n\n".join(extracted_contents))
            return 

        else:
            logger.error(f"Run 失败: {run}")
            return  # 任务未完成时返回 None

    def get_yesterday_chat_list_shop(self, agent_kf):
        with WhisperDB() as db:
            query = """
                SELECT `chat_time`, `chat_name`, `sender`, `act`, `content`
                FROM openai_chat_list
                WHERE SUBSTRING_INDEX(shop_name, ":", 1) = %s AND (`act` = 'ask' OR `act` = 'reply')
                AND DATE(chat_time) = CURDATE() - INTERVAL 1 DAY;
            """
            result = db.query(query, (agent_kf.get_shop_name(),))

        if result:
            result_dict = defaultdict(list)  # 以 chat_name 为 key，值是列表

            for row in result:
                result_dict["会话:" + row[1]].append({
                    "chat_time": row[0].isoformat(),
                    "sender": "客服" if row[2] == "chatGPT" else row[2],
                    "act": row[3],
                    "content": row[4],
                })

            return dict(result_dict)  # 转换回普通字典返回
        return {}  # 返回空字典，而不是 None



