import Head from 'next/head'
import { useRef, useState } from 'react'

const GAMES = ["Arma_3", "Counter_Strike_Global_Offensive", "Counter_Strike", "Dota_2", "Football_Manager_2015", "Garrys_Mod", "Grand_Theft_Auto_V", "Sid_Meiers_Civilization_5", "Team_Fortress_2", "The_Elder_Scrolls_V", "Warframe"]
const GAME_LABEL = GAMES.map((x) => x.replace('_',' ').toUpperCase())

function ReviewData({game_id, username, review, review_url, sentiments}) {
  return (
    <div className='flex flex-col mb-3 overflow-clip'>
      <div className='flex bg-blue-200 w-full'>
        <span className='flex flex-1 px-3 pb-1 pt-2 text-xs'>REVIEW &gt; {GAME_LABEL[game_id]}</span>
        <a className='flex px-3 pb-1 pt-2 text-xs underline' href={review_url} target="_blank">ORIGINAL LINK</a>
      </div>
      <div className='flex bg-blue-100'>
        <div className='flex flex-col items-end w-72 p-3 border-r-[1px] border-black'>
          <span className='font-bold text-xl'>{username}</span>
          <span className='mt-4 text-xs' hidden={sentiments.length < 1}>SENTIMENTS:</span>
          <div className='flex flex-wrap justify-end mt-1'>
            {sentiments.map(([aspect, sentiment]) => (
              <div className={`p-2 rounded-2xl text-xs ml-2 ${sentiment == '+' ? 'bg-green-200' : 'bg-red-200'}`}>
                <span>
                  {sentiment}
                </span>
                <span className='ml-2'>
                  {aspect.toUpperCase()}
                </span>
              </div>
            ))}
          </div>
        </div>
        <div className='flex flex-1 p-3 italic'>
          "{review}"
        </div>
      </div>
    </div>
  )
}

export default function Main() {
  const [filter, setFilter] = useState(Array(GAMES.length).fill(true))
  const [filterVisible, setFilterVisible] = useState(false)
  const [loading, setLoading] = useState(false)
  const [reviewData, setReviewData] = useState([])
  const queryElement = useRef()

  function gameFilterChanged(e) {
    let new_filter = filter
    new_filter[e.target.value] = e.target.checked
    setFilter(new_filter)
  }

  function gameFilterVisibleChanged() {
    setFilterVisible(!filterVisible)
  }

  function queryKeyUp(e) {
    if (e.key == 'Enter') querySend()
  }

  async function querySend() {
    if (loading) return
    let query = queryElement.current.value
    let game_filter = []
    for (const i in filter) {
      if (filter[i] == true) {
        game_filter.push(i)
      }
    }
    setLoading(true)
    try {
      let data = await fetch('http://localhost:8000/api/query?' + new URLSearchParams({
        q: query,
        game_filter: game_filter.join(',')
      })).then((res) => res.json()).then((json_text) => JSON.parse(json_text))
      setReviewData(data)
    } catch (e) {
      console.log(`Fetch failed:\n${e}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col w-full h-screen">
      <Head>
        <title>Steam Review Sentiment Analyzer</title>
      </Head>
      <header className="flex flex-col px-5 pt-7 pb-5 bg-yellow-400">
        <h1 className='font-bold text-2xl mb-1'>
          Steam Review Sentiment Analyzer
        </h1>
        <span className='text-xl'>
          by 13518148, 13519036, 13519147
        </span>
      </header>
      <main className='flex flex-col flex-1 relative bg-neutral-800 overflow-scroll'>
        <div className={`absolute top-[50%] left-[50%] -translate-x-1/2 -translate-y-1/2 w-[30vmin] h-[20vmin] rounded-3xl bg-neutral-900/50 flex flex-col justify-center items-center ${loading ? '' : 'hidden'}`}>
          <div className='border-white border-[8px] w-[8vmin] h-[8vmin] rounded-full border-t-transparent animate-spin'></div>
          <span className='mt-4 text-white text-2xl'>Loading...</span>
        </div>
        <div className='flex flex-col w-full sticky top-0 p-5 backdrop-brightness-[.3] md:px-[20vw]'>
          <span className='flex bg-yellow-200 w-full px-3 pb-1 pt-2 text-xs'>QUERY</span>
          <div className='flex relative'>
            <input ref={queryElement} className='flex-1 py-2 px-3 pr-10 font-bold bg-yellow-100 placeholder:text-yellow-800/40' type="text" placeholder='e.g. graphics' disabled={loading} onKeyUp={queryKeyUp}/>
            <span className='absolute right-0 flex items-center p-2 select-none cursor-pointer' onClick={querySend}>🔍</span>
          </div>
          <div className='flex bg-yellow-200 w-full mt-3'>
            <span className='flex flex-1 px-3 pb-1 pt-2 text-xs'>GAME FILTER</span>
            <a className='flex px-3 pb-1 pt-2 text-xs underline cursor-pointer' onClick={gameFilterVisibleChanged}>{filterVisible ? 'HIDE' : 'SHOW'}</a>
          </div>
          <div className={`flex flex-wrap bg-yellow-100 transition-[max-height] overflow-clip ${filterVisible ? 'max-h-screen' : 'max-h-0'}`}>
            {GAMES.map((x, i) => (
              <div className='flex bg-yellow-100'>
                <input className='ml-3 my-3' id={`game-${x}`} type='checkbox' name='game' value={i} defaultChecked onChange={gameFilterChanged}/>
                <label className='pl-2 py-3 pr-4 select-none hover:underline' for={`game-${x}`}>{x.replaceAll('_',' ')}</label>
              </div>
            ))}
          </div>
        </div>
        <div className='px-10 pt-5 pb-2 md:px-[22%]'>
          {reviewData.map((review) => (
            <ReviewData 
              game_id={review.game_id}
              username={review.username}
              review_url={review.review_url}
              review={review.review}
              sentiments={review.sentiments}
            />
          ))}
        </div>
      </main>
    </div>
  )
}
