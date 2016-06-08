import fetch from 'isomorphic-fetch'
import {
    ADD_TODO,
    TOGGLE_TODO,
    SET_VISIBILITY_FILTER,
    REQUEST_DEPARTMENTS,
    RECEIVE_DEPARTMENTS,
    AUTH_START,
    AUTH_SUCCESS,
    AUTH_FAILED,
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

export const authStart = () => ({
    type: AUTH_START
})

export const authSuccess = () => ({
    type: AUTH_SUCCESS,
// TODO    token: token
})

export const authFailed = (error) => ({
    type: AUTH_FAILED,
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
    dispatch(authStart())
    
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
            dispatch(authSuccess())
        })
}
