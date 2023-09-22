import Signup from './Signup'
import Login from './Login'
import UserDetails from "./UserDetails"

function UserPanel({currentUser, attemptLogin, attemptSignup, logout}) {

  // RENDER //

  if (!currentUser) {

    // render Signup and Login if no currentUser
    return (
        <div className="flex-row">

          <Signup attemptSignup={attemptSignup} />

          <Login attemptLogin={attemptLogin} />

        </div>
      )

    } else {

      // render UserDetails if there's a currentUser
      return (
        <UserDetails currentUser={currentUser} logout={logout} />
      )

    }

}

export default UserPanel
