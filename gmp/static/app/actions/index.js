import fetch from 'isomorphic-fetch'
import {
    ADD_TODO,
    TOGGLE_TODO,
    SET_VISIBILITY_FILTER,
    REQUEST_DEPARTMENTS,
    RECEIVE_DEPARTMENTS,
    LOGIN_REQUEST,
    LOGIN_SUCCESS,
    LOGIN_FAILED,
    LOGOUT_REQUEST,
    LOGOUT_SUCCESS,
    LOGOUT_FAILED,
} from '../constants/index'

let nextId = 0;

export const addTodo = text => ({
    type: ADD_TODO,
    text: text,
    id: nextId++
});

export const toggleTodo = id => ({
    type: TOGGLE_TODO,
    id
});

export const setVisibilityFilter = filter => ({
    type: SET_VISIBILITY_FILTER,
    filter
});

export const requestDepartments = () => ({
    type: REQUEST_DEPARTMENTS
});

export const receiveDepartments = response => ({
    type: RECEIVE_DEPARTMENTS,
    departments: response
});

export const loginRequest = () => ({
    type: LOGIN_REQUEST,
})

export const loginSuccess = () => ({
    type: LOGIN_SUCCESS,
// TODO    token: token
})

export const loginFailed = (error) => ({
    type: LOGIN_FAILED,
    error: error
})

export const logoutRequest = () => ({
    type: LOGOUT_REQUEST
})

export const logoutSuccess = () => ({
    type: LOGOUT_SUCCESS
})

export const logoutFailed = () => ({
    type: LOGOUT_FAILED,
    error: error
})

export const fetchDepartments = () => dispatch => {
    dispatch(requestDepartments())
    return fetch('/api/department/')
        .then(response => response.json(), error => console.log(error))
        .then(json => {
            dispatch(receiveDepartments(json))
        })
}

export const login = (values) => dispatch => {
    dispatch(loginRequest())
    
    return fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: values.email,
                password: values.password
            })
        })
        .then(response => response.json(), error => console.log('Network error:' , error))
        .then(json => {
            console.log('Login data', json)
            dispatch(loginSuccess())
        })
}

export const logout = () => dispatch => {
    dispatch(logoutRequest())
    console.log('logout')
    
    return fetch('/api/logout/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Cookie': 'email: oleynik@mosgmp.ru'
            }
        })
        .then(response =>
            {
                console.log('response')
                response.json()
            }, error => console.log('Network error:' , error))
        .then(json => {
            console.log('Login data', json)
            dispatch(logoutSuccess())
        })
}
