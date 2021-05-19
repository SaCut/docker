# in app.py
@app.route("/flight/", methods=["GET", "POST"])
def flight():
    if request.method == "POST":
        flight = request.form["search"]
        return redirect(url_for("flight_info/" + dict_flights[int(flight)]))
    else:
        return render_template("flight.html", len=len(dict_flights), dict_flights=dict_flights)

# in flight.html
{% extends "base.html" %}

{% block title %}Terminal{% endblock %}



{% block head %}
<link href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
<script src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
{% endblock %}


{% block body %}
<a href="/flight_new/" class="btn btn-primary" tabindex="-1" role="button" aria-disabled="true">New flight</a>

<div class="wrapper fadeInDown">
  <div id="formContent">
    <!-- Tabs Titles -->

    <!-- Login Form -->
    <form action="{{ url_for('flight_info')}}" method="POST" class="login100-form validate-form" id="form1">
        <input type="text" placeholder="Flight ID" name="search" value="{{request.form.search}}">
        <input class="btn btn-default" type="submit" value="Search">
    </form>

  </div>
</div>

<ol>
    {%for i in range(1, len + 1)%}
    <a href="{{ url_for('flight_info', f_id= dict_flights[i].oid) }}">
        <div class="alert alert-dark" role="alert">
        <li>{{dict_flights[i]}}</li>
        </div>
    </a>
    {%endfor%}
</ol>
{% endblock %}