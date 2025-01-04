from channels.generic.websocket import WebsocketConsumer
import json

from api.utils import pinecone_utils

class NavigationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("Connection established")

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        if( not text_data or "rssi" not in text_data):
            self.send(text_data=json.dumps({"message": "No RSSI data provided"}))
            return
        text_data_json = json.loads(text_data)
        print(text_data_json)
        rssi= [ float(i) for i in text_data_json["rssi"]  ]
        index=pinecone_utils.get_vector_store()
        results = index.query(vector=rssi, top_k=1, include_metadata=True)
        point={"id":results["matches"][0]["id"],"location":results["matches"][0]["metadata"]["Location"]} 
        self.send(text_data=json.dumps(point))
         
        