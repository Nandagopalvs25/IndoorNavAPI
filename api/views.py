import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.views import APIView
from api.utils import pinecone_utils

# Create your views here.


def index(request):
    return HttpResponse("Hello welcome to Indoor Navigation  System")



class Node(APIView):
    
    def post(self, request):
         #userr = User.objects.get(id=request.user.id)
        Node_id = request.data["node_id"]
        location = request.data["location"]
        rssi =   [ float(i) for i in request.data["rssi"]  ]
        index=pinecone_utils.get_vector_store()
        data = [
         {"id":Node_id, "values": rssi ,"metadata": {"Location": location}}]
        index.upsert(data)
        #results = vector_store.similarity_search(message,k=5,)
        return HttpResponse("Node Created")
    
    
    def get(self,request):
         if not request.data or "rssi" not in request.data:
           return JsonResponse({"message": "No RSSI data provided"}, status=400)
         try:
            rssi= [ float(i) for i in request.data["rssi"]  ]
            index=pinecone_utils.get_vector_store()
            results = index.query(vector=rssi, top_k=1, include_metadata=True)
            point={"id":results["matches"][0]["id"],"location":results["matches"][0]["metadata"]["Location"]} 
            return JsonResponse(point)
         except:
              return JsonResponse({"message":"Error in processing request"})
         
    
    
    

    
    