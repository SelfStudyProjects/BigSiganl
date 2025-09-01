/*
메인 애플리케이션 컴포넌트
*/
IMPORT React, useState, useEffect
IMPORT Dashboard, Header
IMPORT api from services

FUNCTION App():
    STATE portfolios = []
    STATE loading = true
    STATE error = null
    
    EFFECT on component mount:
        CALL fetchInitialData()
        SET interval for data refresh (30 seconds)
        RETURN cleanup function
    
    FUNCTION fetchInitialData():
        TRY:
            SET loading = true
            data = AWAIT api.getPortfolios()
            SET portfolios = data
            SET loading = false
        CATCH error:
            SET error = error message
            SET loading = false
    
    IF loading:
        RETURN loading spinner
    
    IF error:
        RETURN error message
    
    RETURN:
        <div className="app">
            <Header />
            <Dashboard portfolios={portfolios} />
        </div>