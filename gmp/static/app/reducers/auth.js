import {
    LOGIN_REQUEST, LOGIN_SUCCESS, LOGIN_FAILED,
    LOGOUT_REQUEST, LOGOUT_SUCCESS, LOGOUT_FAILED,

} from '../constants/index'

const auth = (state = {
    isAuthenticated: localStorage.getItem('auth_token') ? true : false,
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
        default:
            return state
    }
}

export default auth
