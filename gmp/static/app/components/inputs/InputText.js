import React from 'react';
import Input from './Input'
import v4 from 'node-uuid'

const InputText = (props) => {
    const id = v4()

    return (
        <Input {...props} id={id}>
            <input
                type={props.type || "text"}
                id={id}
                className="form-control"
                value={props.value}
                onBlur={props.onBlur}
                onChange={props.onChange}
            />
        </Input>
    )
}

export default InputText
