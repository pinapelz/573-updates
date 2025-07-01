import kairosImage from './kairos.png'

export default function NotFound() {
  return (
    <main className="main">
      <div className="content-wrapper">
        <h1 className="title">573 UPDATES</h1>
        <img
          src={kairosImage.src}
          alt="Updates image"
          className="updates-image"
        />
          <>
            <br/>
          <a href="https://arcade.moekyun.me" className="redirect-link">
            you seem lost... lets go back home
          </a>
          </>
      </div>
    </main>
  );
}
