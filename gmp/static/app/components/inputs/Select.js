import React from 'react';
import Input from './Input'
import uuid from 'uuid'

const Select = (props) => {
    const id = uuid.v1()

    return (
        <Input {...props} id={id}>
            <select
                id={id}
                className="form-control"
                value={props.value || ''}
                onBlur={props.onBlur}
                onChange={props.onChange}
            >
                {props.children}
            </select>
        </Input>
    )
}

export default Select
