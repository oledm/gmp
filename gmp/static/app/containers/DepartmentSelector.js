import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import { fetchDepartments } from '../actions/index'
import Select from '../components/inputs/Select'

class DepartmentSelector extends Component {
    constructor(props) {
        super(props)
        props.dispatch(fetchDepartments())
        console.log('DepartmentSelector constructor')
    }

    componentDidMount() {
//        const { dispatch } = this.props
//        dispatch(fetchDepartments())
        console.log('componentDidMount')
        console.log(this.props.options)
    }

    render() {
        return (
            <Select>
                <option value=""></option>
            </Select>
        )
    }
}

const mapStateToProps = (state) => ({
//    options: [{id:1, name: '323232'}, {id:2, name:'fdfsfds'}]
    options: state.departments.departments
})

export default connect(mapStateToProps)(DepartmentSelector)
