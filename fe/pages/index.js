import Head from 'next/head'
import { useState } from 'react'

const GAMES = ["Arma_3", "Counter_Strike_Global_Offensive", "Counter_Strike", "Dota_2", "Football_Manager_2015", "Garrys_Mod", "Grand_Theft_Auto_V", "Sid_Meiers_Civilization_5", "Team_Fortress_2", "The_Elder_Scrolls_V", "Warframe"]
const GAME_LABEL = GAMES.map((x) => x.replace('_',' ').toUpperCase())

function ReviewData({game_id, username, review, review_url, sentiments}) {
  return (
    <div className='flex flex-col mb-3'>
      <div className='flex bg-blue-200 w-full'>
        <span className='flex flex-1 px-3 pb-1 pt-2 text-xs'>REVIEW &gt; {GAME_LABEL[game_id]}</span>
        <a className='flex px-3 pb-1 pt-2 text-xs underline' href={review_url} target="_blank">ORIGINAL LINK</a>
      </div>
      <div className='flex bg-blue-100'>
        <div className='flex flex-col items-end w-72 p-3 border-r-[1px] border-black'>
          <span className='font-bold text-xl'>{username}</span>
          <span className='mt-4 text-xs'>SENTIMENTS:</span>
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

  function gameFilterChanged(e) {
    let new_filter = filter
    new_filter[e.target.value] = !e.target.checked
    setFilter(new_filter)
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
        <div className='flex flex-col w-full sticky top-0 p-5 backdrop-brightness-[.3] md:px-[20vw]'>
          <span className='flex bg-yellow-200 w-full px-3 pb-1 pt-2 text-xs'>QUERY:</span>
          <div className='flex relative'>
            <input className='flex-1 py-2 px-3 pr-10 font-bold bg-yellow-100 placeholder:text-yellow-800/40' type="text" placeholder='e.g. graphics'/>
            <span className='absolute right-0 flex items-center p-2 select-none'>🔍</span>
          </div>
          <span className='flex bg-yellow-200 w-full mt-3 px-3 pb-1 pt-2 text-xs'>GAME FILTER:</span>
          <div className='flex flex-wrap bg-yellow-100'>
            {GAMES.map((x, i) => (
              <div className='flex bg-yellow-100'>
                <input className='ml-3 my-3' id={`game-${x}`} type='checkbox' name='game' value={i} defaultChecked onChange={gameFilterChanged}/>
                <label className='pl-2 py-3 pr-4 select-none hover:underline' for={`game-${x}`}>{x.replaceAll('_',' ')}</label>
              </div>
            ))}
          </div>
        </div>
        <div className='px-10 pt-5 pb-2 md:px-[22%]'>
          <ReviewData 
            game_id={0}
            username="bobbyjenkins"
            review_url="http://steamcommunity.com/id/grizzt/recommended/570/"
            review="The game is fun"
            sentiments={[['graphics quality', '+'], ['gameplay', '-']]}
          />
          <ReviewData 
            game_id={0}
            username="bobbyjenkins"
            review_url="http://steamcommunity.com/id/grizzt/recommended/570/"
            review="The game is fun"
            sentiments={[['graphics quality', '+'], ['gameplay', '-']]}
          />
          <ReviewData 
            game_id={0}
            username="bobbyjenkins"
            review_url="http://steamcommunity.com/id/grizzt/recommended/570/"
            review="The game is fun"
            sentiments={[['graphics quality', '+'], ['gameplay', '-']]}
          />
          <ReviewData 
            game_id={0}
            username="bobbyjenkins"
            review_url="http://steamcommunity.com/id/grizzt/recommended/570/"
            review="The game is fun"
            sentiments={[['graphics quality', '+'], ['gameplay', '-']]}
          />
          <ReviewData 
            game_id={0}
            username="bobbyjenkins"
            review_url="http://steamcommunity.com/id/grizzt/recommended/570/"
            review="The game is fun"
            sentiments={[['graphics quality', '+'], ['gameplay', '-']]}
          />
          <ReviewData 
            game_id={0}
            username="bobbyjenkins"
            review_url="http://steamcommunity.com/id/grizzt/recommended/570/"
            review="The game is fun"
            sentiments={[['graphics quality', '+'], ['gameplay', '-']]}
          />
          <ReviewData 
            game_id={0}
            username="bobbyjenkins"
            review_url="http://steamcommunity.com/id/grizzt/recommended/570/"
            review="The game is fun"
            sentiments={[['graphics quality', '+'], ['gameplay', '-']]}
          />
          <ReviewData 
            game_id={0}
            username="bobbyjenkins"
            review_url="http://steamcommunity.com/id/grizzt/recommended/570/"
            review="The game is fun"
            sentiments={[['graphics quality', '+'], ['gameplay', '-']]}
          />
          <ReviewData 
            game_id={0}
            username="bobbyjenkins"
            review_url="http://steamcommunity.com/id/grizzt/recommended/570/"
            review="The game is fun"
            sentiments={[['graphics quality', '+'], ['gameplay', '-']]}
          />
          <ReviewData 
            game_id={0}
            username="bobbyjenkins"
            review_url="http://steamcommunity.com/id/grizzt/recommended/570/"
            review="The game is fun"
            sentiments={[['graphics quality', '+'], ['gameplay', '-']]}
          />
        </div>
      </main>
    </div>
  )
}
