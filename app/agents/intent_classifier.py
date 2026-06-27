def classify_user_intent(query:str) -> str:
  query = query.lower()
  
  if(
    "flight" in query
    or "aa" in query
    or "status" in query
    or "delayed" in query
    or "gate" in query
    or "departure" in query
    or "arrival" in query
  ):
   return 'flight'
 
  if(
   "baggage" in query 
   or "policy" in query
   or "rebook" in query
   or "connection" in query
 ):
   return "'policy"
 
  if "weather" in query:
    return "weather"
  
  return "general"