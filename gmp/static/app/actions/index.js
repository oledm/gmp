import fetch from 'isomorphic-fetch'
import jwtDecode from 'jwt-decode'
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
    IS_SUBMITTING,
    UPDATE_STORE_USER_DATA,
} from '../constants/index'

let nextId = 0

export const addTodo = text => ({
    type: ADD_TODO,
    text: text,
    id: nextId++
})

export const toggleTodo = id => ({
    type: TOGGLE_TODO,
    id
})

export const setVisibilityFilter = filter => ({
    type: SET_VISIBILITY_FILTER,
    filter
})

export const requestDepartments = () => ({
    type: REQUEST_DEPARTMENTS
})

export const receiveDepartments = response => ({
    type: RECEIVE_DEPARTMENTS,
    departments: response
})

export const loginRequest = (creds) => ({
    type: LOGIN_REQUEST,
    creds
})

export const loginSuccess = (data) => ({
    type: LOGIN_SUCCESS,
    user: data.user
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

export const submitChanged = isSubmitting => ({
    type: IS_SUBMITTING,
    isSubmitting
})

export const updateStoreUserData = data => ({
    type: UPDATE_STORE_USER_DATA,
    data
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
//                    console.log('Login data', data)
                    let token = data.token
                    localStorage.setItem('auth_token', token)

                    let decodedToken = jwtDecode(token)
                    dispatch(loginSuccess(decodedToken))
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
                    let token = data.token
                    localStorage.setItem('auth_token', token)

                    let decodedToken = jwtDecode(token)
                    dispatch(loginSuccess(decodedToken))
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
}

export const updateProfile = (values) => (dispatch, getState) => {
    dispatch(submitChanged(true))
    const { department: {id: depId}, username} = getState().auth.user
    const token = localStorage.getItem('auth_token')
    
    return fetch(`/api/department/${depId}/user/${username}/`, {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': `JWT ${token}`
            },
            body: JSON.stringify({
                first_name: values.first_name,
                last_name: values.last_name,
                middle_name: values.middle_name,
                email: values.email,
                password: values.password
            })
        })
        .then(response => response.json().then(data => ({data, response}))
            .then(({data, response}) => {
                dispatch(submitChanged(false))
                if (!response.ok) {
//                    dispatch(loginFailed('Ошибка! Регистрация не проведена. Неверные имя пользователя или пароль'))
                    console.log('Update failed:', data)
                    return Promise.reject(data)
                } else {
                    console.log('Update success:', data)
                    dispatch(updateStoreUserData(data))
                    return Promise.resolve(data)
                }
            })
        )
        .catch(error => Promise.reject(error))
}

