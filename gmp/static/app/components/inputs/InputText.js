import React from 'react';
import InputWrapper from './InputWrapper'
import InputPure from './InputPure'
//import className from ''
import v4 from 'node-uuid'

const InputText = (props) => {
    const id = v4()

//    const classes = classNames("glyphicon glyphicon-user")

    return (
        <InputWrapper {...props} id={id}>
            {props.icon ? 
                <div className="input-group">
                    <span className="input-group-addon">
                        <i className={"glyphicon glyphicon-" + props.icon}></i>
                    </span>
                    <InputPure id={id} {...props} />
                </div>
                : 
                <InputPure id={id} {...props} />
            }
	</InputWrapper>
    )
}

export default InputText
