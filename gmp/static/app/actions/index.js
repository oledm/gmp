import fetch from 'isomorphic-fetch'
import {
    ADD_TODO,
    TOGGLE_TODO,
    SET_VISIBILITY_FILTER,
    REQUEST_DEPARTMENTS,
    RECEIVE_DEPARTMENTS,
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


export const fetchDepartments = () => dispatch => {
    dispatch(requestDepartments())
    return fetch('http://127.0.0.1:8000/api/department/')
        .then(response => response.json(), error => console.log(error))
        .then(json => {
            dispatch(receiveDepartments(json))
        })
}

export const login = () => dispatch => {
    // loginRequired
    
    return fetch('http://127.0.0.1:8000/api/login/', {
            method: 'POST',
            body: new FormData({
                email: 'oleynik@mosgmp.ru',
                password: 123
            })
        })
        .then(response => response.json(), error => console.log('login error:' , error))
        .then(json => console.log('Login data', json))
}
