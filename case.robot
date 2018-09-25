*** Settings ***
Library    Selenium2Library

*** Test Case ***
Checkin Today
    Login
    Add Row    ${DATE}    _start_=${TIME_NOW}
    Click Element    css=#dgWt_ctl02_btnUpdate

Checkout Today
    Login
    Checkout Row    _end=${TIME_NOW}

Add PTO Today
    Login
    Add PTO    ${DATE}

Add Sick Today
    Login
    Add Sick Leave    ${DATE}

*** Keywords ***
Login
    Open Browser    https://services.htm.co.jp/Login.aspx    PhantomJS
    Input Text    css=#txtUserName    ${USERNAME}
    Input Text    css=#txtPassword    ${PASSWORD}
    Click Button    css=#btnLogin
    Select Frame    main
    Wait Until Keyword Succeeds    5x    2s    Click Element    css=#form1 #btnViewWorkTime

Add Row
    [Arguments]    ${_date}=1/18/2018    ${_start}=9:50 AM    ${_end}=6:45 PM    ${_lunch}=1:30
    Select Frame    list
    Log To Console    ${_date}
    Wait Until Keyword Succeeds    5x    2s    Click Element    css=#btnAddNew
    Wait Until Keyword Succeeds   5x    1s    Input Text    css=#dgWt_ctl02_dtWt_textBox    ${_date}
    Wait Until Keyword Succeeds   5x    1s    Input Text    css=#dgWt_ctl02_txtStartTime    ${_start}
    Wait Until Keyword Succeeds   5x    1s    Input Text    css=#dgWt_ctl02_txtEndTime    ${_end}
    Wait Until Keyword Succeeds   5x    1s    Input Text    css=#dgWt_ctl02_txtLunchDuration   ${_lunch}

Checkout Row
    [Arguments]    ${_end}=6:45 PM
    Select Frame    list
    Log To Console    ${_date}
    Wait Until Keyword Succeeds    5x    2s    Click Element    css=#dgWt_ctl02_btnEdit
    Wait Until Keyword Succeeds   5x    1s    Input Text    css=#dgWt_ctl02_txtEndTime    ${_end}
    Click Element    css=#dgWt_ctl02_btnUpdate

Add PTO
    [Arguments]    ${_date}=1/18/2018
    Add Row    ${_date}
    Wait Until Keyword Succeeds   5x    1s    Input Text    css=#dgWt_ctl02_txtNotes   PTO
    Wait Until Keyword Succeeds   5x    1s    Select From List By Value    css=#dgWt_ctl02_ddlWtTypes  1763
    Click Element    css=#dgWt_ctl02_btnUpdate

Add Sick Leave
    [Arguments]    ${_date}=1/18/2018
    Add Row    ${_date}
    Wait Until Keyword Succeeds   5x    1s    Select From List By Value    css=#dgWt_ctl02_ddlWtTypes  1764
    Click Element    css=#dgWt_ctl02_btnUpdate
