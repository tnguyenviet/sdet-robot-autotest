*** Settings ***
Documentation     Common resources, keywords, and variables for SauceDemo automation tests.
...               This resource file provides shared setup/teardown and common keywords.

Library           SeleniumLibrary    timeout=10s    implicit_wait=5s
Library           Collections
Library           String
Library           OperatingSystem

# Custom Libraries
Library           libraries.pages.LoginPage              WITH NAME    Login
Library           libraries.utils.AutomationLogger       WITH NAME    Logger
Library           libraries.utils.BrowserManager         WITH NAME    Browser

*** Variables ***
# Base Configuration
${BASE_URL}                 https://www.saucedemo.com
${BROWSER}                  chrome
${HEADLESS}                 true
${IMPLICIT_WAIT}            10s
${SELENIUM_TIMEOUT}         10s

# Test Credentials
${STANDARD_USER}            standard_user
${LOCKED_USER}              locked_out_user
${PROBLEM_USER}             problem_user
${PERFORMANCE_USER}         performance_glitch_user
${PASSWORD}                 secret_sauce

# Expected Messages
${MSG_LOCKED_OUT}           Sorry, this user has been locked out
${MSG_INVALID_CREDS}        Username and password do not match
${MSG_USERNAME_REQUIRED}    Username is required
${MSG_PASSWORD_REQUIRED}    Password is required

*** Keywords ***
# ==================== Setup & Teardown Keywords ====================

Open Browser To SauceDemo
    [Documentation]    Opens browser and navigates to SauceDemo login page.
    [Arguments]    ${browser}=${BROWSER}    ${headless}=${HEADLESS}
    ${is_headless}=    Evaluate    '${headless}'.lower() == 'true'
    Browser.Open Chrome To URL    ${BASE_URL}    headless=${is_headless}
    Wait Until Page Contains Element    id=login-button    timeout=${SELENIUM_TIMEOUT}

Close Browser And Cleanup
    [Documentation]    Closes browser and performs cleanup.
    Capture Page Screenshot On Failure
    Close All Browsers

Capture Page Screenshot On Failure
    [Documentation]    Captures screenshot if test failed.
    Run Keyword If Test Failed    Capture Page Screenshot

# ==================== Login Keywords ====================

Login As Standard User
    [Documentation]    Logs in with standard user credentials.
    Login To SauceDemo    ${STANDARD_USER}    ${PASSWORD}
    Verify Successful Login

Login As Locked User
    [Documentation]    Attempts login with locked out user.
    Login.Login With Credentials    ${LOCKED_USER}    ${PASSWORD}

Login As Problem User
    [Documentation]    Logs in with problem user credentials.
    Login To SauceDemo    ${PROBLEM_USER}    ${PASSWORD}

Login As Performance User
    [Documentation]    Logs in with performance glitch user.
    Login To SauceDemo    ${PERFORMANCE_USER}    ${PASSWORD}

Login To SauceDemo
    [Documentation]    Generic login keyword with credentials.
    [Arguments]    ${username}    ${password}
    Login.Verify Login Page Is Displayed
    Login.Login With Credentials    ${username}    ${password}

Verify Successful Login
    [Documentation]    Verifies login was successful by checking URL.
    Wait Until Page Contains Element    css=.inventory_list    timeout=${SELENIUM_TIMEOUT}
    Location Should Contain    inventory

Verify Login Failed With Message
    [Documentation]    Verifies login failed with expected error message.
    [Arguments]    ${expected_message}
    Login.Login Error Should Be Visible
    ${error}=    Login.Get Login Error Message
    Should Contain    ${error}    ${expected_message}
