import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import api from "../api"
import styles from "./Dashboard.module.css"

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    api.get("/dashboard")
      .then(res => setData(res.data))
      .catch(err => {
        if (err.response?.status === 401) {
          localStorage.removeItem("token")
          navigate("/login")
        }
      })
      .finally(() => setLoading(false))
  }, [])

  const logout = () => {
    localStorage.removeItem("token")
    navigate("/login")
  }

  return (
    <div className={styles.page}>
      <nav className={styles.nav}>
        <div className={styles.logo}>⚡ JobSync</div>
        <div className={styles.navLinks}>
          <button onClick={() => navigate("/match")} className={styles.navBtn}>Upload Resume</button>
          <button onClick={logout} className={styles.navBtn}>Logout</button>
        </div>
      </nav>

      <div className={styles.container}>
        <h1 className={styles.title}>Your Dashboard</h1>
        {loading && <p className={styles.loading}>Loading...</p>}

        {data && (
          <>
            <div className={styles.statsRow}>
              <div className={styles.statCard}>
                <div className={styles.statNum}>{data.total_uploads}</div>
                <div className={styles.statLabel}>Resumes Uploaded</div>
              </div>
              <div className={styles.statCard}>
                <div className={styles.statNum}>{data.history[0]?.skills?.length || 0}</div>
                <div className={styles.statLabel}>Skills Detected (Latest)</div>
              </div>
            </div>

            <h2 className={styles.sectionTitle}>Upload History</h2>

            {data.history.length === 0 ? (
              <div className={styles.empty}>
                <p>No resumes uploaded yet.</p>
                <button className={styles.btn} onClick={() => navigate("/match")}>Upload Your First Resume</button>
              </div>
            ) : (
              <div className={styles.historyList}>
                {data.history.map((r) => (
                  <div key={r.resume_id} className={styles.historyCard}>
                    <div className={styles.historyTop}>
                      <span className={styles.filename}>📄 {r.filename}</span>
                      <span className={styles.date}>{new Date(r.uploaded_at).toLocaleDateString()}</span>
                    </div>
                    <div className={styles.skills}>
                      {r.skills.slice(0, 10).map(s => (
                        <span key={s} className={styles.skill}>{s}</span>
                      ))}
                      {r.skills.length > 10 && <span className={styles.more}>+{r.skills.length - 10} more</span>}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}