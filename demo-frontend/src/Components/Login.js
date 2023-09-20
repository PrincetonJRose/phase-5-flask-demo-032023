import { useState } from 'react'
import './Login.css'

const initialState = {
    email: '',
    password: ''
}

const Login = ({ closeLoginModal, loginUser }) => {

    const [ formData, setFormData ] = useState( initialState )

    const updateFormData = ( event ) => {
        const { name, value } = event.target
        const changeFormData = { ...formData, [ name ]: value }
        setFormData( changeFormData )
    }

    return (
        <form
            id="myModal"
            className="modal"
            onSubmit = { ( event ) => {
                event.preventDefault()
                loginUser( formData )
                setFormData( initialState )
            }}
        >
            {/* <!-- Modal content --> */}
            <div className="modal-content">
            <span
                className="close"
                onClick = { closeLoginModal }
            >&times;</span>
                <label>
                    Email:
                </label>
                <input 
                    type='text'
                    name='email'
                    value = { formData.email }
                    onChange = { updateFormData }
                />
                <br/>
                <label>
                    Password:
                </label>
                <input
                    type = 'password'
                    name = 'password'
                    value = { formData.password }
                    onChange = { updateFormData }
                />
                <br/>
                <button type = 'submit'>Login</button>
            </div>
        </form>
    )
}

export default Login