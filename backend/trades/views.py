"""
거래 관련 API 뷰
"""
CLASS TradeListView(ListCreateAPIView):
    METHOD get():
        FILTER trades by date range (optional)
        FILTER by asset (optional)
        ORDER by timestamp DESC
        PAGINATE results
        RETURN serialized data
    
    METHOD post():
        VALIDATE incoming trade data
        SAVE to database
        TRIGGER portfolio recalculation
        RETURN created trade

CLASS TradeDetailView(RetrieveAPIView):
    METHOD get():
        GET trade by ID
        RETURN serialized trade data

CLASS LatestTradesView(ListAPIView):
    METHOD get():
        GET last 20 trades
        RETURN serialized data