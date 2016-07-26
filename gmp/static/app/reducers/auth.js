import jwtDecode from 'jwt-decode'
import {
    LOGIN_REQUEST, LOGIN_SUCCESS, LOGIN_FAILED,
    LOGOUT_REQUEST, LOGOUT_SUCCESS, LOGOUT_FAILED,
    UPDATE_STORE_USER_DATA,

} from '../constants/index'

const token = localStorage.getItem('auth_token') 

let user 
if (token) {
    user = jwtDecode(token).user
}

const auth = (state = {
    isAuthenticated: token ? true : false,
    user: user,
    isPending: false
}, action) => {
    switch(action.type) {
        case LOGIN_REQUEST:
            return {...state,
                isPending: true,
                creds: action.creds
            }
        case LOGIN_SUCCESS:
            return {...state,
                isPending: false,
                isAuthenticated: true,
                user: action.user
            }
        case LOGIN_FAILED:
        case LOGOUT_FAILED:
            return {...state,
                isPending: false,
                error: action.error
            }
        case LOGOUT_REQUEST:
            return {...state,
                isPending: true
            }
        case LOGOUT_SUCCESS:
            return {...state,
                isPending: false,
                isAuthenticated: false
            }
        case UPDATE_STORE_USER_DATA:
            return {...state,
                user: {...state.user, ...action.data}
            }
        default:
            return state
    }
}

export default auth
