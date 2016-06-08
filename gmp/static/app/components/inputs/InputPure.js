import React from 'react'

const InputPure = (props) => (
    <input
        type={props.type || "text"}
        id={props.id}
        className="form-control"
        value={props.value}
        onBlur={props.onBlur}
        onChange={props.onChange}
    />
)

export default InputPure
