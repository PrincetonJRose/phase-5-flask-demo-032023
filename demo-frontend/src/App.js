import logo from './logo.svg';
import './App.css';
import { useState, useEffect } from 'react'
import Login from './Components/Login'

const baseUrl = 'http://127.0.0.1:3000'
const ingredientsUrl = baseUrl + '/ingredients'
const recipesUrl = baseUrl + '/recipes'

function App() {

  const [ ingredients, setIngredients ] = useState( [] )
  const [ recipes, setRecipes ] = useState( [] )
  const [ recipe, setRecipe ] = useState( null )
  const [ currentUser, setCurrentUser ] = useState( null )
  const [ toggleLoginForm, setToggleLoginForm ] = useState( false )

  const fetchIngredients = () =>
    fetch( ingredientsUrl )
    .then( r => r.json() )
    .then( setIngredients )

  const fetchRecipes = () =>
    fetch( recipesUrl )
    .then( r => r.json() )
    .then( setRecipes )

  const fetchRecipe = ( id ) =>
    fetch( recipesUrl + '/' + id )
    .then( r => r.json() )
    .then( setRecipe )

  useEffect( () => {
    window.onclick = ( event ) => {
      if ( event.target.classList.contains( 'modal' ) ) {
        setToggleLoginForm( false )
      }
    }
  }, [] )

  useEffect( () => {
    const uuid = localStorage.getItem( 'uuid' )
    if ( uuid ) {
      fetch( baseUrl + '/autologin/' + uuid )
      .then( r => {
        if ( r.ok )
          r.json().then( setCurrentUser )
      })
    }
  }, [] )

  const loginUser = ( loginInfo ) => {
    
    const postRequest = {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'accept': 'application/json',
      },
      body: JSON.stringify( loginInfo )
    }
    
    fetch( baseUrl + '/login', postRequest )
    .then( r => r.json() )
    .then( user => {
      if ( user.errors )
        alert( user.errors[0] )
      else {
        setCurrentUser( user )
        localStorage.uuid = user.id
        closeLoginModal()
      }
    })
  }

  const closeLoginModal = ( ) => {
    setToggleLoginForm( false )
  }

  const logoutUser = ( ) => {
    if ( currentUser ) {
      fetch( baseUrl + '/logout' )
      setCurrentUser( null )
      localStorage.removeItem( 'uuid' )
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <br/>
        {
          currentUser ?
            <button
              onClick = { logoutUser }
            >Logout</button>
          :
            <button
              onClick = { () => setToggleLoginForm( true ) }
            >Login</button>
        }
        
        {
          toggleLoginForm ?
            <Login 
              loginUser = { loginUser }
              closeLoginModal = { closeLoginModal }
            />
          : null
        }

        <br/>
        <button onClick={ fetchIngredients }>Hit me to fetch ingredients!</button>
        <br/>
        { 
          currentUser ?
            <button onClick = { fetchRecipes } >Hit me to fetch recipes!</button>
          : null
        }

      </header>
    </div>
  );
}

export default App;
