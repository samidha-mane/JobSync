import { useState } from "react"
import { useNavigate } from "react-router-dom"
import api from "../api"
import styles from "./Match.module.css"

export default function Match() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const navigate = useNavigate()

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    setError("")
    setResult(null)
    try {
      const form = new FormData()
      form.append("file", file)
      const res = await api.post("/match", form)
      setResult(res.data)
    } catch (err) {
      if (err.response?.status === 401) {
        localStorage.removeItem("token")
        navigate("/login")
      }
      setError(err.response?.data?.detail || "Something went wrong")
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem("token")
    navigate("/login")
  }

  return (
    <div className={styles.page}>
      <nav className={styles.nav}>
        <div className={styles.logo}>⚡ JobSync</div>
        <div className={styles.navLinks}>
          <button onClick={() => navigate("/dashboard")} className={styles.navBtn}>Dashboard</button>
          <button onClick={logout} className={styles.navBtn}>Logout</button>
        </div>
      </nav>

      <div className={styles.container}>
        <div className={styles.hero}>
          <h1>Find Your Perfect Job Match</h1>
          <p>Upload your resume and let AI match you with real jobs</p>
        </div>

        <div className={styles.uploadCard}>
          <form onSubmit={handleUpload}>
            <div className={styles.dropzone} onClick={() => document.getElementById("fileInput").click()}>
              {file ? (
                <div className={styles.fileSelected}>
                  <span>📄</span>
                  <span>{file.name}</span>
                </div>
              ) : (
                <div className={styles.dropPrompt}>
                  <span className={styles.uploadIcon}>☁️</span>
                  <p>Click to upload your resume</p>
                  <p className={styles.hint}>PDF files only</p>
                </div>
              )}
            </div>
            <input id="fileInput" type="file" accept=".pdf" style={{display:"none"}} onChange={e => setFile(e.target.files[0])} />
            <button className={styles.btn} type="submit" disabled={!file || loading}>
              {loading ? "Analyzing..." : "Match My Resume"}
            </button>
          </form>
        </div>

        {error && <div className={styles.error}>{error}</div>}

        {result && (
          <div className={styles.results}>
            <div className={styles.skillsCard}>
              <h3>Extracted Skills</h3>
              <div className={styles.skills}>
                {result.extracted_skills.map(skill => (
                  <span key={skill} className={styles.skill}>{skill}</span>
                ))}
              </div>
            </div>

            <h3 className={styles.matchTitle}>
              {result.total_matches} Job Matches Found
            </h3>

            <div className={styles.jobs}>
              {result.matches.map((job) => (
                <div key={job.job_id} className={styles.jobCard}>
                  <div className={styles.jobHeader}>
                    <div>
                      <h4 className={styles.jobTitle}>{job.title}</h4>
                      <p className={styles.jobCompany}>{job.company} · {job.location}</p>
                    </div>
                    <div className={styles.scoreCircle} style={{
                      background: job.match_score >= 70 ? "#166534" : job.match_score >= 50 ? "#713f12" : "#1e1b4b"
                    }}>
                      <span>{job.match_score}%</span>
                    </div>
                  </div>

                  {job.matched_skills.length > 0 && (
                    <div className={styles.skillSection}>
                      <p className={styles.skillLabel}>✅ Matched</p>
                      <div className={styles.skills}>
                        {job.matched_skills.map(s => <span key={s} className={styles.skillGreen}>{s}</span>)}
                      </div>
                    </div>
                  )}

                  {job.missing_skills.length > 0 && (
                    <div className={styles.skillSection}>
                      <p className={styles.skillLabel}>❌ Missing</p>
                      <div className={styles.skills}>
                        {job.missing_skills.map(s => <span key={s} className={styles.skillRed}>{s}</span>)}
                      </div>
                    </div>
                  )}

                  {job.source_url && (
                    <a href={job.source_url} target="_blank" rel="noreferrer" className={styles.applyBtn}>
                      Apply Now →
                    </a>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}