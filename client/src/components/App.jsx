import { useState, useEffect } from 'react'
import UserPanel from "./UserPanel"
import Notes from "./Notes"

const POST_HEADERS = {
  'Content-Type': 'application/json',
  'Accepts': 'application/json'
}

const URL = "/api/v1"

function App() {

  // STATE //

  const [currentUser, setCurrentUser] = useState(null)

  useEffect(() => {
    async function checkSession() {
      const response = await fetch(URL + '/check_session')

      if (response.ok) {
        const data = await response.json()
        setCurrentUser( data )
      }
    }
    checkSession()
  }, [])


  // SIGNUP, LOGIN AND LOGOUT FNS //

  async function attemptSignup(userInfo) {
    const res = await fetch(URL + '/users', {
      method: 'POST',
      headers: POST_HEADERS,
      body: JSON.stringify(userInfo)
    })
    if (res.ok) {
      const data = await res.json()
      setCurrentUser(data)
    } else {
      alert('Invalid sign up')
    }
  }

  async function attemptLogin(userInfo) {
    const res = await fetch(URL + '/login', {
      method: 'POST',
      headers: POST_HEADERS,
      body: JSON.stringify(userInfo)
    })
    if (res.ok) {
      const data = await res.json()
      setCurrentUser(data)
    } else {
      alert('Invalid sign up')
    }
  }

  function logout() {
    setCurrentUser(null)
    fetch(URL + '/logout', {
      method: 'DELETE'
    })
  }


  // RENDER //

  return (
    <div className="App">

      <h1>Authentication + Authorization</h1>

      <UserPanel
      currentUser={currentUser}
      attemptLogin={attemptLogin}
      attemptSignup={attemptSignup}
      logout={logout} />

      <Notes currentUser={currentUser} />

    </div>
  );
}

export default App;
