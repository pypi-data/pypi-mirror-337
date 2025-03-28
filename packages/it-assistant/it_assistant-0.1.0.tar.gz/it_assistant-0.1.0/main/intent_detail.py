# -*- coding: utf-8 -*-
import http.client
import json
import time
import requests
headers = {
    'cookie': 'X-Kunlun-SessionId=L%3A9b9b8a418a3e44ee93be.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2YWwiOnsidGVuYW50X2lkIjozOTAsInVzZXJfaWQiOjE3MjIxNjYwNzMxOTk2NDUsInRlbmFudF9kb21haW5fbmFtZSI6ImFwYWFzIiwic2Vzc2lvbl92ZXJzaW9uIjoidjIwMjAtMDUtMTkiLCJ3c190b2tlbiI6Ilc6MmI3OWVmNTNlMjliNDJkMDliOWYiLCJsb2dpbl90b2tlbiI6IjE3MDE3ZmFlMWJlNjVlMzd1OFVhMzA0ZjY0N2MyZmFjY2QwWmk5YmNmNGVjNzAzZDgwOWYxNG9TZzY0MzY1ZjEyNWI0YmZlZDhMMVkiLCJzb3VyY2VfY2hhbm5lbCI6ImZlaXNodSIsInRlbmFudF9rZXkiOiI3MzY1ODhjOTI2MGYxNzVkIiwiZXh0ZXJuYWxfZG9tYWluX25hbWUiOiJieXRlZGFuY2UiLCJvcmlnaW5hbF90ZW5hbnRfaWQiOjAsIm9yaWdpbmFsX3VzZXJfaWQiOjAsImlkcF9jaGFubmVsIjoiIn0sImV4cCI6MTc1Nzc0ODAyNn0.jtRwvfjo202TfxaKGUmuMfsnxGFCqh0uJeaU0WzU9y4; trust_browser_id=3686a9b0-ce48-4e07-a0ce-e6928dc2bd6a; X-Kunlun-LoginTag=feishu; passport_trace_id=7389204030662426627; passport_web_did=7424353640858812419; QXV0aHpDb250ZXh0=9bcf0657fb6e47d497625011ffcd73e7; lark_sso_session=XN0YXJ0-488md350-54b2-433e-9eeb-b7a5c700ea26-WVuZA; X-Larkgw-Web-DID=3439857258174095984; X-Larkgw-Use-Lark-Session-119=1; __tea__ug__uid=7441424216023565850; is_anonymous_session=; fid=24c45ffc-f3d7-44f2-87ed-421f54ee78fb; lang=zh; i18n_locale=zh; locale=zh-CN; _gcl_au=1.1.2073766041.1742190427; session=XN0YXJ0-58dm27f7-6609-4cf5-a569-b398d3908dab-WVuZA; session_list=XN0YXJ0-58dm27f7-6609-4cf5-a569-b398d3908dab-WVuZA; kunlun-session-v2=L%3A9b9b8a418a3e44ee93be.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2YWwiOnsidGVuYW50X2lkIjozOTAsInVzZXJfaWQiOjE3MjIxNjYwNzMxOTk2NDUsInRlbmFudF9kb21haW5fbmFtZSI6ImFwYWFzIiwic2Vzc2lvbl92ZXJzaW9uIjoidjIwMjAtMDUtMTkiLCJ3c190b2tlbiI6Ilc6MmI3OWVmNTNlMjliNDJkMDliOWYiLCJsb2dpbl90b2tlbiI6IjE3MDE3ZmFlMWJlNjVlMzd1OFVhMzA0ZjY0N2MyZmFjY2QwWmk5YmNmNGVjNzAzZDgwOWYxNG9TZzY0MzY1ZjEyNWI0YmZlZDhMMVkiLCJzb3VyY2VfY2hhbm5lbCI6ImZlaXNodSIsInRlbmFudF9rZXkiOiI3MzY1ODhjOTI2MGYxNzVkIiwiZXh0ZXJuYWxfZG9tYWluX25hbWUiOiJieXRlZGFuY2UiLCJvcmlnaW5hbF90ZW5hbnRfaWQiOjAsIm9yaWdpbmFsX3VzZXJfaWQiOjAsImlkcF9jaGFubmVsIjoiIn0sImV4cCI6MTc1Nzc0ODAyNn0.jtRwvfjo202TfxaKGUmuMfsnxGFCqh0uJeaU0WzU9y4; kunlun-session-token=b1313c24b034f057a020e874a925dbafcf7c55da5ad8480d95bbf9b1d42deec5; _tea_utm_cache_1229=undefined; msToken=iku1uGx14pDdoSF8p_uY6JqnwvVgDW1ndE8oBJoef4phzoeBc_L2PRV3z6hd2XtAn7AMujKo1wXnH0s8vy3wbTTyhITMmYzNkSb021QSjr6Pf_0VxsCsvzrrgv3XBO9Y5Imioh6cXi6CfcmZDsGssHgD_dKL6kFDoCknvP0UyhEo; lgw_csrf_token=da7a4edc7f25f70d9691e711baf68d45206af9f5-1742543686; _uuid_hera_ab_path_1=7484185668152180739; _csrf_token=d85786e2b7c1581fb43064bf6a90ea52a7c79389-1742547774; Hm_lvt_a79616d9322d81f12a92402ac6ae32ea=1742547770,1742549581; landing_url=https%3A%2F%2Fwww.feishu.cn%2F; _uetvid=44545540063311f08ed91353a6123699; _ga_7PY069DX7K=GS1.1.1742549605.1.0.1742549605.60.0.0; _ga=GA1.2.113646166.1700115833; _ga_VPYRHN104D=GS1.1.1742547771.2.1.1742549614.28.0.0; passport_app_access_token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDI4NDA5NDcsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtX2FjY2Vzc19pbmZvIjp7IjEwNyI6eyJpYXQiOjE3NDI3OTc3NDcsImFjY2VzcyI6dHJ1ZX19LCJzdW0iOiI1YmU3NWI1ZjhmMmQ1MDczYWEzMTdjZDU1MDMxMmVhODY4MzVlMWE0ZGEyYjk3Y2U2Nzk3NjEwYzEyNThmZjQyIn19.9hXltmyyAZ_JWuyS0T2ZgKBIufxp2JsrXw3IgZPyC6oTR1UlNz1XJ4WZCI6XTnR_mndrchQmzBCrunlvT-4pFg; swp_csrf_token=6bbaee45-b520-4d23-bd2a-7e79e06f0a2e; t_beda37=ed89cb8b75dc13a3818811a31b65fd2f66f80217f2a157a326a0bebb6c4fdba7; sl_session=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDI4NDE1NDMsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtZXRhIjoiQVdIazBuRzhRUUFDQUFBQUFBQUFBQUZuQ0pwTTZrU0FBMmNJbWt6cVJJQURaeklSUnZpQUFBRUNLZ0VBUVVGQlFVRkJRVUZCUVVKdU1UZGtiVEV3YUVGQmR6MDkiLCJzdW0iOiI1YmU3NWI1ZjhmMmQ1MDczYWEzMTdjZDU1MDMxMmVhODY4MzVlMWE0ZGEyYjk3Y2U2Nzk3NjEwYzEyNThmZjQyIiwibG9jIjoiemhfY24iLCJhcGMiOiJSZWxlYXNlIiwiaWF0IjoxNzQyNzk4MzQzLCJzYWMiOnsiVXNlclN0YWZmU3RhdHVzIjoiMSIsIlVzZXJUeXBlIjoiNDIifSwibG9kIjpudWxsLCJjbmYiOnsiamt0IjoiS05RVm4yRVlsNDlONDAteTZQalJ1OEdFSHNNSDI4NUM0MFJNODNxRjBoayJ9LCJucyI6ImxhcmsiLCJuc191aWQiOiI3MDUzOTk0MzAyMzAwNTUzMjE4IiwibnNfdGlkIjoiMSIsIm90IjozLCJjdCI6MTc0MjE5MDQzOSwicnQiOjE3NDI3ODEzMDh9fQ.Ud5vohxo4Kv7w00dHxX47BPaXYS1oBNnYmSotjk7lbggv7ZyVeMSGBi0Y4X0sjIT2BP4hY7ZySkXgFdLhuL-YA',
    'x-kunlun-token': '17017fae1be65e37u8Ua304f647c2faccd0Zi9bcf4ec703d809f14oSg64365f125b4bfed8L1Y',
    'Content-Type': 'application/json'
}
itamheaders = {
  'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6InYyIiwidHlwIjoiSldUIn0.eyJleHAiOjE3NDI1NDYyMTcsImp0aSI6ImJKMk9hV0dkanU5QStMMXciLCJpYXQiOjE3NDEyNTAyMTcsImlzcyI6InRhbm5hIiwic3ViIjoiMzgzMDMxOUBieXRlZGFuY2UucGVvcGxlIiwidGVuYW50X2lkIjoiYnl0ZWRhbmNlLnBlb3BsZSIsInRlbmFudF9uYW1lIjoiIiwicHJvamVjdF9rZXkiOiJjcm1TZmdIVmU1dXhIMHJyIiwidW5pdCI6ImV1X25jIiwiYXV0aF9ieSI6Mn0.eHghtX4NOnD1uD65bzqv7n1J3mtnPPXJoVKIWDwl4PMZPkqc3FisH4RMXxDqeOyDCgRHYhmam7VEenl8T0UIKpzI8ad8yMiZytvAkNhclLjCdmokLB7DdwnbO1qeDLxdqjL-S3da0KHHkOT8j-rWR94XJ0N7T_snoko4Ovsp13w',
  'Content-Type': 'application/json'

}

class webapiClient:
    def __init__(self):
        """
       初始化 Client 实例,tenant_access_token 会在 Client 初始化时自动获取
        """
        self.headers = headers
        self.itamheaders = headers
        self.conn = http.client.HTTPSConnection("apaas.feishu.cn")

    def get_intent_detail_list(self, startAt,pageSize):
        """
        outdata:
            对话ID 技能分发 用户输入
           res_ = {
          'intentID': 7485259579248705537,
          'skillLabels': ["GUI 设备/配件申请"],
          'userInput': "我要申请一个鼠标",
           'apply_day':"",
          'apply_num':"",
          'asset_name':"",
          'device_type':""
           }
        """
        endAt = int(time.time())
        payload = json.dumps({
            "startAt": startAt,
            "endAt": endAt,
            "matchIntentID": "",
            "matchStatus": [],
            "pageSize": pageSize+10
        })
        self.conn.request("POST",
                          "/ai/api/v1/conversational_runtime/namespaces/spring_f17d05d924__c/stats/intent_detail_list",
                          payload, self.headers)
        res = self.conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))
        res_list = []

        for i in data['data']['intentDetailList']:
            if i['channelType'] in ["LARK_OPEN_API","LARK_BOT","ANONYMOUS_CUI_SDK"]:
                res_list.append(
                    {'intentID': i['intentID'], 'skillLabels': i['skillLabels'], 'userInput': i['userInput']})
        return res_list

    def get_intent_detail_llm(self, res_list):
        """
        提取关键词
        'apply_day': "",'apply_num': "",'asset_name': "",'device_type': ""
        """
        res_list_out = [{
            'intentID': 7485264011232886786,
            'userInput': "我要申请一个鼠标",
            'skillLabels': ["GUI 设备/配件申请"],
           }
        ]
        payload = ''
        for i in res_list:
            #关键词的提取 初始化
            i['apply_day'] = 'NULL'
            i['apply_num'] = 'NULL'
            i['asset_name'] = 'NULL'
            i['device_type'] = 'NULL'
            intentID = i['intentID']
            urlintentID = f'https://apaas.feishu.cn/ai/api/v1/conversational_runtime/namespaces/spring_f17d05d924__c/intent/{intentID}?pageSize=20&statusFilter=%5B%5D&fieldFilter=_node_id&fieldFilter=status&fieldFilter=usages&fieldFilter=_node_name&fieldFilter=_node_type&fieldFilter=title_for_maker&fieldFilter=associate_id'
            response = requests.request("GET", urlintentID, headers=self.headers, data=payload)
            response = json.loads(response.text)
            for j in response['data']['steps']:
                if j['titleForMaker'] in ["槽位抽取","LLM 2"]:
                    nodeid = j['nodeID']
                    urlnodeid = f'https://apaas.feishu.cn/ai/api/v1/conversational_runtime/namespaces/spring_f17d05d924__c/association/{intentID}/node/{nodeid}?intentID={intentID}'
                    response = requests.request("GET", urlnodeid, headers=self.headers, data=payload)
                    data_nodeid = json.loads(response.text)
                    nodeid_output = json.loads(data_nodeid['data']['step']['output'])
                    if nodeid_output is not None and nodeid_output['response'] is not None:
                        i['apply_day'] = nodeid_output['response'].get('apply_day', 'NULL')
                        i['apply_num'] = nodeid_output['response'].get('apply_num', 'NULL')
                        i['asset_name'] = nodeid_output['response'].get('asset_name', 'NULL')
                        i['device_type'] = nodeid_output['response'].get('device_type', 'NULL')
        return res_list

    def get_bestmatchitemforreturn(self,keyword):
        """
        mock数据，获取最佳匹配的sku/spu
        mock数据：公用配件列表、设备列表、软件列表
        todo：mock数据表格为飞书文档或者其他？
        """
        _urlGetBestMatchItemForReturn = "https://asset-mig-pre.bytedance.net/aily/api/itservice/ai/GetBestMatchItemForReturn"

        payload = json.dumps({
            "SearchKey": keyword,
            "AiUseType": 1,
            "ListReturnableAccessoryRequest": {
                "IsAll": True,
                "Page": {
                    "PageNum": 1,
                    "PageSize": 30
                },
                "OwnerUserID": "",
                "AccessoryApplyTypeList": []
            },
            "GetAssetListRequest": {
                "Status": 6,
                "Search": "",
                "IsAll": True,
                "SubStatusList": [
                    12,
                    18,
                    19
                ],
                "Page": {
                    "PageNum": 1,
                    "PageSize": 30
                },
                "OrganizationalUnitID": 1
            }
        })
        response = requests.request("GET", _urlGetBestMatchItemForReturn, headers=self.headers, data=payload)
        response = json.loads(response.text)

    def get_segsearchcandidates(self, res_list):
        #获取分数值
        ### 读取设备&配件的信息并拼接到text里面
        ### 遍历res_list中的device_name
        ###判断是否在asset.json里面
        ###调用算法接口获取设备&配件的分数值
        pass



if __name__ == '__main__':
    data = webapiClient().get_intent_detail_list(1742227200)
    data_qqq = webapiClient().get_intent_detail_llm(data)
    print("成都")
