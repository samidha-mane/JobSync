import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import api from "../api"
import styles from "./Auth.module.css"

export default function Login() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError("")
    try {
      const res = await api.post("/auth/login", { email, password })
      localStorage.setItem("token", res.data.access_token)
      navigate("/match")
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.logo}>⚡ JobSync</div>
        <h2 className={styles.title}>Welcome back</h2>
        <p className={styles.sub}>Sign in to your account</p>
        {error && <div className={styles.error}>{error}</div>}
        <form onSubmit={handleSubmit} className={styles.form}>
          <input className={styles.input} type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
          <input className={styles.input} type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
          <button className={styles.btn} disabled={loading}>{loading ? "Signing in..." : "Sign In"}</button>
        </form>
        <p className={styles.switch}>Don't have an account? <Link to="/signup">Sign up</Link></p>
      </div>
    </div>
  )
}