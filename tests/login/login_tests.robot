*** Settings ***
Documentation     Login functionality tests for SauceDemo.
...               Tests cover valid login, invalid login scenarios, and edge cases.
...               
...               Test Data:
...               - Standard user: standard_user / secret_sauce
...               - Locked user: locked_out_user (should fail with locked message)
...               - Invalid credentials should show error message

Resource          ../../resources/keywords/common.resource

Suite Setup       Log    Starting Login Test Suite
Suite Teardown    Close All Browsers

Force Tags        login

*** Test Cases ***
Valid Login With Standard User
    [Documentation]    Verify user can login with valid credentials.
    [Tags]    smoke    positive    critical
    Open Browser To SauceDemo
    Login.Verify Login Page Is Displayed
    Login.Login With Credentials    ${STANDARD_USER}    ${PASSWORD}
    Verify Successful Login

Valid Login With Performance Glitch User
    [Documentation]    Verify performance user can login (slower response).
    [Tags]    positive
    Open Browser To SauceDemo
    Login To SauceDemo    ${PERFORMANCE_USER}    ${PASSWORD}
    Verify Successful Login

Invalid Login With Wrong Password
    [Documentation]    Verify login fails with incorrect password.
    [Tags]    negative    security
    Open Browser To SauceDemo
    Login.Login With Credentials    ${STANDARD_USER}    wrong_password
    Verify Login Failed With Message    ${MSG_INVALID_CREDS}

Invalid Login With Wrong Username
    [Documentation]    Verify login fails with non-existent username.
    [Tags]    negative    security
    Open Browser To SauceDemo
    Login.Login With Credentials    invalid_user    ${PASSWORD}
    Verify Login Failed With Message    ${MSG_INVALID_CREDS}

Invalid Login With Empty Username
    [Documentation]    Verify login fails when username is empty.
    [Tags]    negative    validation
    Open Browser To SauceDemo
    Login.Input Password    ${PASSWORD}
    Login.Click Login Button
    Verify Login Failed With Message    ${MSG_USERNAME_REQUIRED}

Invalid Login With Empty Password
    [Documentation]    Verify login fails when password is empty.
    [Tags]    negative    validation
    Open Browser To SauceDemo
    Login.Input Username    ${STANDARD_USER}
    Login.Click Login Button
    Verify Login Failed With Message    ${MSG_PASSWORD_REQUIRED}

Invalid Login With Empty Credentials
    [Documentation]    Verify login fails when both fields are empty.
    [Tags]    negative    validation
    Open Browser To SauceDemo
    Login.Click Login Button
    Verify Login Failed With Message    ${MSG_USERNAME_REQUIRED}

Locked User Cannot Login
    [Documentation]    Verify locked out user receives appropriate error.
    [Tags]    negative    security
    Open Browser To SauceDemo
    Login As Locked User
    Verify Login Failed With Message    ${MSG_LOCKED_OUT}

Login Error Can Be Dismissed
    [Documentation]    Verify error message can be closed.
    [Tags]    ui
    Open Browser To SauceDemo
    Login.Click Login Button
    Login.Login Error Should Be Visible
    Login.Dismiss Login Error
    Login.Login Error Should Not Be Visible

Login Form Can Be Cleared
    [Documentation]    Verify login form fields can be cleared.
    [Tags]    ui
    Open Browser To SauceDemo
    Login.Input Username    ${STANDARD_USER}
    Login.Input Password    ${PASSWORD}
    Login.Clear Login Form
    Login.Verify Username Field Is Empty
    Login.Verify Password Field Is Empty

