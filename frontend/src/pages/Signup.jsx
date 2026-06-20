import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import api from "../api"
import styles from "./Auth.module.css"

export default function Signup() {
  const [form, setForm] = useState({ email: "", full_name: "", password: "" })
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError("")
    try {
      await api.post("/auth/signup", form)
      const res = await api.post("/auth/login", { email: form.email, password: form.password })
      localStorage.setItem("token", res.data.access_token)
      navigate("/match")
    } catch (err) {
      setError(err.response?.data?.detail || "Signup failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.logo}>⚡ JobSync</div>
        <h2 className={styles.title}>Create account</h2>
        <p className={styles.sub}>Start matching your resume to real jobs</p>
        {error && <div className={styles.error}>{error}</div>}
        <form onSubmit={handleSubmit} className={styles.form}>
          <input className={styles.input} type="text" placeholder="Full Name" value={form.full_name} onChange={e => setForm({...form, full_name: e.target.value})} required />
          <input className={styles.input} type="email" placeholder="Email" value={form.email} onChange={e => setForm({...form, email: e.target.value})} required />
          <input className={styles.input} type="password" placeholder="Password" value={form.password} onChange={e => setForm({...form, password: e.target.value})} required />
          <button className={styles.btn} disabled={loading}>{loading ? "Creating..." : "Create Account"}</button>
        </form>
        <p className={styles.switch}>Already have an account? <Link to="/login">Sign in</Link></p>
      </div>
    </div>
  )
}