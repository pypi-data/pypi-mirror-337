# -*- coding: utf-8 -*-

from main.ailyapp_client import AilyLarkClient
from main.lark_client import LarkdocsClient
from main.intent_detail import *
import datetime

#Testsuitelink = "https://bytedance.larkoffice.com/sheets/ZVzfsw4rMhkMF6tjtxmc4BdSnMb"


def do_ai_auto(Testsuitelink):
    startAt = 0
    tenant_access_token = AilyLarkClient().get_tenant_access_token()
    # 通过文档链接获取spreadsheet_token
    spreadsheet_token = str.split(Testsuitelink, "/")[-1]
    # 读取表格用户输入，并
    spreadsheet = LarkdocsClient().get_the_worksheet(spreadsheet_token)
    for i in spreadsheet.sheets:
        column_count = i.grid_properties.column_count
        row_count = i.grid_properties.row_count
        sheet_id = i.sheet_id
        title = i.title
        # print(column_count, row_count, sheet_id, title)
        # json_str = {"ranges": ["459f7e!A1:A1"]}
        json_str = {"ranges": [sheet_id + "!A1:A" + str(row_count)]}
        test = LarkdocsClient().get_plaintextcontent(json_str, spreadsheet_token, sheet_id)
        test = json.loads(test)
        userinput = test['data']['value_ranges'][0]['values']
        print(f"表头为{userinput[0]}")
        for i in range(1, row_count):
            if userinput[i][0]:
                if startAt == 0:
                    startAt = int(time.time())
                seseion_id = AilyLarkClient().create_ailysession(tenant_access_token)
                message_id = AilyLarkClient().create_ailysessionaily_message(tenant_access_token, seseion_id,
                                                                             userinput[i][0])
                runs = AilyLarkClient().create_ailysession_run(tenant_access_token, seseion_id)
                time.sleep(1)
            else:
                return startAt,i
                break


def get_conversationlogs(startAt):
    """
    对话ID 技能分发 用户输入
    res_data = {
            'intentID': 7485259579248705537,
            'skillLabels': ["GUI 设备/配件申请"],
            'userInput': "我要申请一个鼠标",

         }
         """
    data = webapiClient().get_intent_detail_list(startAt)


def write_reslut(data, Testsuitelink, title):
    """
    写入表格
    """
    #创建工作表
    spreadsheet_token = str.split(Testsuitelink, "/")[-1]
    sheetinfo= {"index": 0, "title": title + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}
    spreadsheet0 = LarkdocsClient().createsheets(spreadsheet_token, sheetinfo)
    sheet_id = spreadsheet0['sheet_id']
    #创建表头
    dicta = {"value_ranges": [
        {"range": f"{sheet_id}!A1:A1", "values": [[[{"text": {"text": "序号"}, "type": "text"}]]]}]}
    for key in data[0].keys():
        dicta["value_ranges"].append(
            {"range": f"{sheet_id}!{chr(ord('A') + len(dicta['value_ranges']))}1:{chr(ord('A') + len(dicta['value_ranges']))}1",
             "values": [[[{"text": {"text": key}, "type": "text"}]]]})
    spreadsheet1 = LarkdocsClient().writesheets(spreadsheet_token, sheet_id, dicta)
    #写入数据
    for i in range(len(data)):
        dicta = {"value_ranges": [
            {"range": f"{sheet_id}!A{i + 2}:A{i + 2}", "values": [[[{"text": {"text": i + 1}, "type": "text"}]]]}]}
        for key in data[i].keys():
            dicta["value_ranges"].append(
                {"range": f"{sheet_id}!{chr(ord('A') + len(dicta['value_ranges']))}{i + 2}:{chr(ord('A') + len(dicta['value_ranges']))}{i + 2}",
                 "values": [[[{"text": {"text": str(data[i][key])}, "type": "text"}]]]})
        LarkdocsClient().writesheets(spreadsheet_token, sheet_id, dicta)



if __name__ == '__main__':
    Testsuitelink = "https://bytedance.larkoffice.com/sheets/ZVzfsw4rMhkMF6tjtxmc4BdSnMb"
    startAt,num = do_ai_auto(Testsuitelink)
    data = webapiClient().get_intent_detail_list(startAt,20)
    data_qqq = webapiClient().get_intent_detail_llm(data)
    aaaa = write_reslut(data_qqq, Testsuitelink, "测试")



