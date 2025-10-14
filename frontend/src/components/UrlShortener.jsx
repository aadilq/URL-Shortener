import React, { useState } from 'react'; 


const UrlShortener = () => {
    const [url, setUrl] = useState(''); //Input URL value
    const [resultUrl, setresultUrl] = useState(''); //Result shortened URL
    const [loading, setloading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) =>{
        e.preventDefault();

        setresultUrl(null);
        setError('');
        setloading(true);

        try{
            const response = await fetch('http://localhost:8000/api/shorten_url', {
                method: 'POST', 
                headers: {
                    'content-type': 'applications/json'
                }, 
                body: JSON.stringify({ url: url })
            });

            if(!response.ok){
                throw new Error('Failed to shorten the URL');
            }
            const data = await response.json();
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
                    <button onClick={()=> navigator.clipboard.writeText(resultUrl.shorten_url)}>
                        Copy
                    </button>
                </div>
            )}
        </div>
    )
}

export default UrlShortener;