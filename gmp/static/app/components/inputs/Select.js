import React from 'react';
import InputWrapper from './InputWrapper'
import v4 from 'node-uuid'

const Select = (props) => {
    const id = v4()

    return (
        <InputWrapper {...props} id={id}>
            <select
                id={id}
                className="form-control"
                value={props.value || ''}
                onBlur={props.onBlur}
                onChange={props.onChange}
            >
                {props.children}
            </select>
        </InputWrapper>
    )
}

export default Select
