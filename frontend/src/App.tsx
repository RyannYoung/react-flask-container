import { faSearch, faSpinner } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState } from "react";
import { useSpring, animated, useTransition } from "react-spring";
import logo from "./logo.svg";

interface IResponse {
  message: string;
  status: string;
}

const App = () => {
  const [res, setRes] = useState<IResponse>();
  const [scrape, setScrape] = useState("");
  const [show, setShow] = useState(false);

  async function handleClick() {
    setShow(true);
    try {
      const res = await fetch("http://localhost:5000/");
      const json = await res.json();
      setRes(json);
    } catch (error) {
      setRes({
        message: String(error),
        status: "error",
      });
    }
  }

  const anim = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    delay: 1000,
  });

  const transition = useTransition(show, {
    from: { opacity: 0 },
    enter: { opacity: 1 },
  });

  return (
    <div className="w-screen h-screen flex justify-center">
      <div className="w-full max-w-4xl h-fit mt-24">
        <animated.img
          style={anim}
          src={logo}
          className="h-36 self-center mx-auto"
          alt="logo"
        />
        <section className="prose">
          <h1>React-Flask App</h1>
          <p>
            A template design for a full-stack application which includes both
            React (frontend) and Flask (backend)
          </p>
        </section>
        <div className="my-2 flex items-center gap-x-2">
          <div
            className="tooltip"
            data-tip="Send a request to the Flask API to test it's functionality!"
          >
            <button
              className={`btn btn-sm border-0 ${
                show && res
                  ? res?.status != "error"
                    ? "bg-green-500  hover:bg-green-600"
                    : "bg-red-500 hover:bg-red-600"
                  : "bg-orange-500 hover:bg-orange-600"
              }`}
              onClick={handleClick}
            >
              {show && !res ? (
                <FontAwesomeIcon
                  icon={faSpinner}
                  className="animate-spin mr-2"
                />
              ) : null}
              Test API
            </button>
          </div>
          {transition((style, item) =>
            item ? (
              <animated.code style={style}>{JSON.stringify(res)}</animated.code>
            ) : null
          )}
        </div>
        <section>
          <div className="flex">
            <div className="w-full">
              <label className="label">
                <span className="label-text">Scrape URL/File Upload</span>
              </label>
              <div className="flex flex-col gap-2 w-full">
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="https://example.com"
                    className="input input-bordered flex-1"
                  />
                  <div className="divider-vertical divider">OR</div>
                  <input
                    type="file"
                    accept=".csv, .txt"
                    className="file:rounded-md file:btn flex-1"
                  />
                </div>
                <button className="btn">
                  <FontAwesomeIcon icon={faSearch} className="mr-2" />
                  Scrape
                </button>
              </div>
            </div>
          </div>
        </section>
        <div className="divider">Backend Response</div>
        <section className="prose">
          <h2>Backend Response</h2>
        </section>
        {scrape ? (
          <div>{scrape}</div>
        ) : (
          <p>
            Currently no content has been scraped/queued, add a url or upload a
            file then click search!
          </p>
        )}
      </div>
    </div>
  );
};

export default App;
