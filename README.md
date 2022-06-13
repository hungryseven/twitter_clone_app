<h1>twitter_clone_app</h1>
<h2>Intro</h2>
<p>This project represents an attempt to develop twitter copy with following stack:</p>
<ul>
  <li>Django 4</li>
  <li>PostgreSQL</li>
  <li>Vanilla JS</li>
  <li>Bootstrap</li>
</ul>
<h2>Available functionality</h2>
<p>The following functionality is currently available:</p>
<ul>
  <li>Simple registration without email or phone confirmation and authentication</li>
  <li>Tweet system close to the original. It includes replies, likes, retweets and tree hierarchy.</li>
  <li>User profiles with the ability to follow/unfollow each other.</li>
  <li>Bookmarks and notifications.</li>
  <li>Search tweets and users system.</li>
  <li>And a bunch of other small features which available in original twitter.</li>
</ul>
<h2>Heroku</h2>
<p>The project was deployed on heroku and currently available. At the moment i'm trying to attach cloud storage to serve media files e.g. profile photos.</p>
<p><a href="https://poor-twitter-clone.herokuapp.com/">Go to project start page</a></p>
<p>Follow the link to watch profiles with content:</p>
<ul>
  <li><a href="https://poor-twitter-clone.herokuapp.com/alexandr_sem/">My own profile</a></li>
  <li><a href="https://poor-twitter-clone.herokuapp.com/administrator/">Admin profile</a></li>
</ul>
<p>
  Authenticate with admin credentials below to try project and get access to <a href="https://poor-twitter-clone.herokuapp.com/admin/">admin-panel</a>:
</p>
<ul>
  <li><strong>Login</strong> - administrator</br></li>
  <li><strong>Password</strong> - admin</li>
</ul>
<h2>Docker</h2>
<p>If you want to run app locally, follow the commands below.</p>
<p>Stop your local postgres server to avoid possible conflicts.</p>
<p><strong>1.</strong> <i>Clone the repo</i></p>
<code>git clone https://github.com/hungryseven/twitter_clone_app.git</code>
<p></p>
<p><strong>2.</strong> <i>Create image and start containers</i></p>
<code>docker compose up -d --build</code>
<p></p>
<p><strong>3.</strong> <i>Restore db from backup or apply migrations</i></p>
<p>Restore db from backup:</p>
<code>docker exec -i twitter_clone_db psql -U postgres -d twitter_clone < backup.sql</code>
<p></p>
<p>Apply migrations:</p>
<code>docker compose exec web python manage.py migrate</code>
<p></p>
<p><strong>4.</strong> <i>Open app in your browser</i></p>
<a href="http://127.0.0.1:8000/">Main page</a></br>
<a href="http://127.0.0.1:8000/alexandr_sem/">My profile</a></br>
<a href="http://127.0.0.1:8000/administrator/">Admin profile</a></br>
<a href="http://127.0.0.1:8000/admin/">Admin-panel</a>
<p></p>
<p><strong>5.</strong> <i>Keep your device clean</i></p>
<p>Stop and remove containers and volume:</p>
<code>docker compose down -v</code>
<p></p>
<p>Remove image:</p>
<code>docker rmi twitter_clone_web</code>
