import React, { useState } from 'react'; 


const UrlShortener = () => {
    const [url, setUrl] = useState(''); //Input URL value
    const [resultUrl, setresultUrl] = useState(''); //Result shortened URL
    const [loading, setloading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) =>{
        console.log('handleSubmit called!');
        e.preventDefault();

        setresultUrl(null);
        setError('');
        setloading(true);

        console.log("Sending URL: ", url)
        console.log("Request body:", JSON.stringify({url: url}))

        try{
            const response = await fetch('http://localhost:8000/api/shorten_url', {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json'
                }, 
                body: JSON.stringify({ url: url })
            });
            console.log('Response status:', response.status);
            const data = await response.json();
            console.log('Response data:', data);

            if(!response.ok){
                throw new Error('Failed to shorten the URL');
            }
            setresultUrl(data)
        }
        catch(error){
            setError(error.message)
        }
        finally{
            setloading(false)
        }
    }
    return(
        <div>
            <h1>URL Shortener</h1>

            <form onSubmit={handleSubmit}>
                <input
                type='url'
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder='Enter your long URL here' 
                required
                className='border-1 border-white-100 mr-4 w-full mt-4 mb-4'
                />
                <button type='submit' disabled={loading}>
                    {loading ? "Shortening..." : "Shorten URL"}
                </button>
            </form>
            {error && (
                <div style={{color: "red"}}>
                    Error: {error}
                </div>
            )}

            {resultUrl && (
                <div>
                    <p>Shortened URL:</p>
                    <a href={resultUrl.shorten_url} target='_blank' rel="noopener noreferrer">
                        {resultUrl.shorten_url}
                    </a>
                    <button className="mr-4" onClick={()=> navigator.clipboard.writeText(resultUrl.shorten_url)}>
                        Copy
                    </button>
                </div>
            )}
        </div>
    )
}

export default UrlShortener;