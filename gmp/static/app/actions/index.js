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
    ROUTING,
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

export const loginRequest = (creds) => ({
    type: LOGIN_REQUEST,
    creds
})

export const loginSuccess = (authData) => ({
    type: LOGIN_SUCCESS,
    authData
})

export const loginFailed = (error) => ({
    type: LOGIN_FAILED,
    error
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

export const redirectTo = url => dispatch => {
    dispatch({
        type: ROUTING,
        method: 'push',
        nextUrl: url
    })
}

export const login = (values) => dispatch => {
    dispatch(loginRequest(values))
    
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
        .then(response => response.json().then(data => ({data, response}))
            .then(({data, response}) => {
                if (!response.ok) {
                    dispatch(loginFailed('Ошибка! Неверные имя пользователя или пароль'))
                    return Promise.reject(data)
                } else {
                    console.log('Login data', data)
                    localStorage.setItem('auth_token', data.token)
                    dispatch(loginSuccess(data))
                    dispatch(redirectTo('/'))
                }
            })
        )
        .catch(error => console.error('Error:', error))
}

export const register = (values) => dispatch => {
    dispatch(loginRequest(values))
    
    return fetch(`/api/department/${values.department}/user/`, {
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
        .then(response => response.json().then(data => ({data, response}))
            .then(({data, response}) => {
                if (!response.ok) {
                    dispatch(loginFailed('Ошибка! Регистрация не проведена. Неверные имя пользователя или пароль'))
                    return Promise.reject(data)
                } else {
                    console.log('Login data after register', data)
                    localStorage.setItem('auth_token', data.token)
                    dispatch(loginSuccess(data))
                    dispatch(redirectTo('/'))
                }
            })
        )
        .catch(error => console.error('Error:', error))
}

export const logout = () => dispatch => {
    dispatch(logoutRequest())
    localStorage.removeItem('auth_token')
    dispatch(logoutSuccess())
//    console.log('logout')
//    
//    return fetch('/api/logout/', {
//            method: 'POST',
//            credentials: 'same-origin',
//            headers: {
//                'Accept': 'application/json',
//                'Content-Type': 'application/json',
//                'Cookie': 'email: oleynik@mosgmp.ru'
//            }
//        })
//        .then(response =>
//            {
//                console.log('response')
//                response.json()
//            }, error => console.log('Network error:' , error))
//        .then(json => {
//            console.log('Login data', json)
//            dispatch(logoutSuccess())
//        })
}

