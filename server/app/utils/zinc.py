import base64
import requests
import json
class Zinc (object) :
    def __init__ (self) :
        self.user=''
        self.pwd=''
        self.host=''
        self.indexTag=''
        self.searchDict={}
    def setApp (self,app) :
        self.user=app.config.get('ZINC_USER')
        self.pwd=app.config.get('ZINC_PWD')
        self.host=app.config.get('ZINC_HOST')
        return True
    def insert (self,data,id='') :
        url=self.host+'/api/'+self.indexTag+'/_doc'
        if(id!=''):
            url=url+'/'+id
        res = requests.put(url=url,data=data.encode('utf-8'), headers=self.authHeader()).json()
        return res
    def index (self,index) :
        self.indexTag=index
        return self
    def field (self,field) :
        self.searchDict['_source']=field
        return self
    def where (self,query) :
        self.searchDict['query']=query
        return self
    def order (self,order) :
        self.searchDict['sort']=order
        return self
    def limit (self,start,pager) :
        self.searchDict['from']=start
        self.searchDict['max_results']=pager 
        return self
    def query (self,**kwargs) :
        print(self.searchDict)
        res = requests.post(url=self.host+'/api/'+self.indexTag+'/_search',data=json.dumps(self.searchDict).encode('utf-8'), headers=self.authHeader()).json()
        if "raw" in kwargs and kwargs['raw']==True:
            result=res['hits']['hits']
        else:
            result = list(map(lambda x: dict({'_id':x['_id']},**x['_source']), res['hits']['hits'])) 
        return {"total":res['hits']['total']['value'],"res":result}
    def search (self,**kwargs) :
        if "sep" in kwargs and kwargs['sep']==True:
            self.searchDict['search_type']='querystring'
        else:
            self.searchDict['search_type']='matchphrase'
        res = requests.post(url=self.host+'/api/'+self.indexTag+'/_search',data=json.dumps(self.searchDict).encode('utf-8'), headers=self.authHeader()).json()
        if "raw" in kwargs and kwargs['raw']==True:
            result=res['hits']['hits']
        else:
            result = list(map(lambda x: dict({'_id':x['_id']},**x['_source']), res['hits']['hits'])) 
        return {"total":res['hits']['total']['value'],"res":result}
    def delete (self,id) :
        res = requests.delete(url=self.host+'/api/'+self.indexTag+'/_doc/'+id, headers=self.authHeader()).json()
        return res
    def deleteIndex (self) :
        res = requests.delete(url=self.host+'/api/index/'+self.indexTag, headers=self.authHeader()).json()
        return res
    def insertAll (self,data) :
        res = requests.post(url=self.host+'/api/'+self.indexTag+'/_multi',data=data.encode('utf-8'), headers=self.authHeader()).json()
        return res
    def authHeader (self) :
        return {"Authorization": "Basic {}".format(str(base64.b64encode(bytes(self.user+':'+self.pwd, encoding='utf-8')), 'utf-8'))}