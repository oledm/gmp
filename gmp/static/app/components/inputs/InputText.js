import React from 'react';
import Input from './Input'
import uuid from 'uuid'


const InputText = (props) => {
    const id = uuid.v1()

    return (
        <Input {...props} id={id}>
            <input
                type="text"
                id={id}
                className="form-control"
                required={!props.optional}
                value={props.value}
                onBlur={props.onBlur}
                onChange={props.onChange}
            />
        </Input>
    )
}

export default InputText
