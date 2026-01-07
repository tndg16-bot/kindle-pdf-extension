import { useState } from 'react'
import './App.css'

// LINE URL
const LINE_URL = 'https://lin.ee/VAYurUv'

// 選択肢の型定義
interface QuestionOption {
  text: string
  type?: string
  skill?: string
  time?: string
}

interface Question {
  id: number
  question: string
  options: QuestionOption[]
}

// 質問データ
const questions: Question[] = [
  {
    id: 1,
    question: 'もし1日だけ有名人になれるとしたら、何をする？',
    options: [
      { text: 'ベストセラー作家として本にサインする', type: 'writer' },
      { text: 'アーティストとして作品を発表する', type: 'creator' },
      { text: '講演会で1000人の前で話す', type: 'consultant' },
      { text: '自分が作ったサービスを世界に発表する', type: 'builder' },
    ],
  },
  {
    id: 2,
    question: '理想の休日の過ごし方は？',
    options: [
      { text: '一人でカフェで読書や考え事', type: 'writer' },
      { text: '美術館やおしゃれスポットでインスピレーション', type: 'creator' },
      { text: '友人とビジネスや人生について語る', type: 'consultant' },
      { text: '家でDIYや新しいツールを試す', type: 'builder' },
    ],
  },
  {
    id: 3,
    question: 'この中で一番手に入れたいものは？',
    options: [
      { text: '安定した副収入', type: 'writer' },
      { text: '自分の作品が評価される喜び', type: 'creator' },
      { text: '人から「すごい」と言われる実績', type: 'consultant' },
      { text: '自分で何かを生み出す達成感', type: 'builder' },
    ],
  },
  {
    id: 4,
    question: '今のPC/AIスキルは？',
    options: [
      { text: 'ほぼ初心者、SNSくらい', skill: 'beginner' },
      { text: '基本的な操作はできる、Excelなど', skill: 'intermediate' },
      { text: 'ChatGPTなど使ったことある', skill: 'ai-user' },
      { text: 'プログラミングやデザインもできる', skill: 'advanced' },
    ],
  },
  {
    id: 5,
    question: '自分一人の自由な時間は、週にどれくらい？',
    options: [
      { text: '5時間未満（ほとんどない）', time: 'minimal' },
      { text: '5〜10時間', time: 'moderate' },
      { text: '10〜20時間', time: 'good' },
      { text: '20時間以上', time: 'plenty' },
    ],
  },
]


// 診断結果データ
const results = {
  writer: {
    emoji: '🖊️',
    title: 'ライター型',
    tagline: '言葉で人の心を動かす才能',
    description: '一人でじっくり考え、文章で表現することが得意なあなた。情報を整理し、わかりやすく伝える力があります。AIを活用すれば執筆スピードが3倍に。',
    jobs: ['AIライティング（ブログ記事、SEO記事）', 'コピーライティング（LP、広告文）', 'SNS運用代行', '電子書籍執筆'],
    mbti: ['INFJ', 'INFP', 'INTJ', 'INTP'],
    firstStep: 'ChatGPTで1記事書いてみる',
    color: '#6366f1',
  },
  creator: {
    emoji: '🎨',
    title: 'クリエイター型',
    tagline: 'ビジュアルで世界観を創る才能',
    description: '美的センスがあり、見た目のインパクトを大切にするあなた。「映える」コンテンツを生み出す力があります。AI画像生成で、アイデアを一瞬で形にできる時代です。',
    jobs: ['AI画像生成（SNS素材、サムネイル）', '動画編集（ショート動画、YouTube）', 'Webデザイン', 'NFTアート'],
    mbti: ['ISFP', 'ENFP', 'ESFP', 'ISTP'],
    firstStep: 'MidjourneyやCanva AIで1枚作ってみる',
    color: '#ec4899',
  },
  consultant: {
    emoji: '🎤',
    title: 'コンサル型',
    tagline: '人を導き、影響を与える才能',
    description: '人と話すのが好きで、相手の悩みを解決したいあなた。「すごい」と言われたい気持ちが原動力になります。AIで知識武装すれば、専門家としての発信力が倍増。',
    jobs: ['AI活用コンサルティング', 'オンライン講座・セミナー講師', 'コーチング', '情報発信（YouTube、Note）'],
    mbti: ['ENFJ', 'ENTJ', 'ENTP', 'ESTP'],
    firstStep: '自分の経験を1つの「教え」にまとめてみる',
    color: '#f59e0b',
  },
  builder: {
    emoji: '🔧',
    title: 'ビルダー型',
    tagline: 'ゼロから形を創る才能',
    description: '仕組みを作ったり、新しいツールを試すのが好きなあなた。「自分で作った」という達成感が最高のご褒美。AIとノーコードで、エンジニアでなくてもプロダクトが作れる時代です。',
    jobs: ['AIツール開発（GPTs、自動化ツール）', 'Webサイト制作', 'アプリ開発（ノーコード）', '業務効率化コンサル'],
    mbti: ['INTJ', 'INTP', 'ISTJ', 'ISTP'],
    firstStep: '自分用の便利ツールを1つAIで作ってみる',
    color: '#10b981',
  },
}

type ResultType = keyof typeof results
type Screen = 'start' | 'quiz' | 'result'

function App() {
  const [screen, setScreen] = useState<Screen>('start')
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<string[]>([])
  const [result, setResult] = useState<ResultType | null>(null)
  const [showMBTI, setShowMBTI] = useState(false)
  const [selectedMBTI, setSelectedMBTI] = useState('')

  const startQuiz = () => {
    setScreen('quiz')
  }

  const handleAnswer = (type: string) => {
    const newAnswers = [...answers, type]
    setAnswers(newAnswers)

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else {
      // 結果を計算
      const typeCounts: Record<string, number> = {}
      newAnswers.forEach((answer) => {
        if (answer in results) {
          typeCounts[answer] = (typeCounts[answer] || 0) + 1
        }
      })

      const resultType = Object.entries(typeCounts).sort((a, b) => b[1] - a[1])[0]?.[0] as ResultType || 'writer'
      setResult(resultType)
      setScreen('result')
    }
  }

  const restart = () => {
    setScreen('start')
    setCurrentQuestion(0)
    setAnswers([])
    setResult(null)
    setShowMBTI(false)
    setSelectedMBTI('')
  }

  const progress = ((currentQuestion + 1) / questions.length) * 100

  // スタート画面
  if (screen === 'start') {
    return (
      <div className="app">
        <div className="background-effects">
          <div className="blob blob-1"></div>
          <div className="blob blob-2"></div>
        </div>

        <div className="start-container">
          <div className="start-card glass-card">
            <div className="start-header">
              <span className="start-emoji">🤖</span>
              <h1 className="start-title">AI副業適性診断</h1>
              <p className="start-subtitle">あなたに向いているAI副業がわかる！</p>
            </div>

            <div className="start-features">
              <div className="feature-item">
                <span className="feature-icon">⏱️</span>
                <span>たった1分</span>
              </div>
              <div className="feature-item">
                <span className="feature-icon">❓</span>
                <span>5問の質問</span>
              </div>
              <div className="feature-item">
                <span className="feature-icon">🎯</span>
                <span>4タイプ判定</span>
              </div>
            </div>

            <p className="start-description">
              簡単な質問に答えるだけで、<br />
              あなたの才能と相性の良いAI副業がわかります。
            </p>

            <button className="start-btn" onClick={startQuiz}>
              🚀 診断スタート
            </button>

            <p className="start-note">※ 診断は無料です</p>
          </div>
        </div>
      </div>
    )
  }

  // 結果画面
  if (screen === 'result' && result) {
    const data = results[result]
    return (
      <div className="app">
        <div className="background-effects">
          <div className="blob blob-1" style={{ background: data.color }}></div>
          <div className="blob blob-2"></div>
        </div>

        <div className="result-container">
          <div className="result-card glass-card">
            <div className="result-header" style={{ color: data.color }}>
              <span className="result-emoji">{data.emoji}</span>
              <h1 className="result-title">あなたは「{data.title}」です</h1>
            </div>

            <p className="result-tagline">{data.tagline}</p>
            <p className="result-description">{data.description}</p>

            <div className="result-section">
              <h3>💼 向いているAI副業</h3>
              <ul className="job-list">
                {data.jobs.map((job, i) => (
                  <li key={i}>{job}</li>
                ))}
              </ul>
            </div>

            <div className="result-section">
              <h3>🧠 相性の良いMBTI</h3>
              <div className="mbti-tags">
                {data.mbti.map((m) => (
                  <span key={m} className="mbti-tag">{m}</span>
                ))}
              </div>

              {!showMBTI && (
                <button className="mbti-input-btn" onClick={() => setShowMBTI(true)}>
                  MBTIを入力してさらに詳しく分析 →
                </button>
              )}

              {showMBTI && (
                <div className="mbti-input">
                  <select
                    value={selectedMBTI}
                    onChange={(e) => setSelectedMBTI(e.target.value)}
                    className="mbti-select"
                  >
                    <option value="">MBTIを選択</option>
                    {['INTJ', 'INTP', 'ENTJ', 'ENTP', 'INFJ', 'INFP', 'ENFJ', 'ENFP',
                      'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ', 'ISTP', 'ISFP', 'ESTP', 'ESFP'].map(m => (
                        <option key={m} value={m}>{m}</option>
                      ))}
                  </select>
                  {selectedMBTI && (
                    <p className="mbti-result">
                      {data.mbti.includes(selectedMBTI)
                        ? `✅ ${selectedMBTI}は${data.title}と相性抜群！`
                        : `💡 ${selectedMBTI}のあなたも${data.title}で活躍できます！詳しくはLINEで解説中`
                      }
                    </p>
                  )}
                </div>
              )}
            </div>

            <div className="result-section">
              <h3>🚀 おすすめの第一歩</h3>
              <p className="first-step">{data.firstStep}</p>
            </div>

            <div className="cta-section">
              <h3>🎁 LINE登録で追加特典！</h3>
              <ul className="cta-list">
                <li>✅ あなたのタイプ専用ロードマップPDF</li>
                <li>✅ MBTIタイプ別 × AI副業 詳細分析</li>
                <li>✅ 初回相談無料（通常¥5,000）</li>
              </ul>
              <a href={LINE_URL} target="_blank" rel="noopener noreferrer" className="cta-button" style={{ background: data.color }}>
                👇 今すぐ受け取る
              </a>
            </div>

            <button className="restart-btn" onClick={restart}>
              もう一度診断する
            </button>
          </div>
        </div>
      </div>
    )
  }

  // 質問画面
  const question = questions[currentQuestion]

  return (
    <div className="app">
      <div className="background-effects">
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
      </div>

      <div className="quiz-container">
        <div className="quiz-header">
          <span className="quiz-logo">🤖</span>
          <span className="quiz-title">AI副業適性診断</span>
        </div>

        <div className="quiz-card glass-card">
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }}></div>
          </div>
          <p className="progress-text">質問 {currentQuestion + 1} / {questions.length}</p>

          <h2 className="question-text">{question.question}</h2>

          <div className="options">
            {question.options.map((option, index) => (
              <button
                key={index}
                className="option-btn"
                onClick={() => handleAnswer(option.type || option.skill || option.time || '')}
              >
                {option.text}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
