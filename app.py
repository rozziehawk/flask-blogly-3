"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import User, Post, Tag, PostTag, db, connect_db, asc, desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
#db.create_all()


@app.route("/")
def display_users():
    return redirect("/users", code=302)
#def display_home():
#    """Show homepage."""
#
#    return render_template("index.html")


@app.route('/users')
def list_users():
    """Renders directory of employees and phone numbers  (from dept)"""
    users = User.query.order_by(asc(User.last_name)).order_by(User.first_name).all()
    return render_template('users.html', users=users)

@app.route('/users/<userid>')
def user_detail(userid):
    """Renders individual user detail page"""
    user = User.query.get(userid)
    print (f"inside user_detail, userid = {userid}")
    return render_template('user_detail.html', user=user)

@app.route("/user_action/<userid>", methods=["POST"])
def user_action(userid):
    user = User.query.get(userid)
    which_button = request.form['edit_delete']
    print(f"Inside user_action, userid={userid}, request={which_button}")
    if (which_button == 'Edit'):
        return render_template('user_edit_form.html', user=user)
    else: #must be delete
        User.query.filter_by(id=userid).delete()
        db.session.commit()
        return redirect("/users", code=302)                   
    #print(request.form)
    #print(request.form['edit_delete'])
    #return render_template('user_detail.html', user=user)

@app.route("/user_edit/<userid>", methods=["POST"])
def save_user_edit(userid):
    user = User.query.get(userid)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit() 
    #print (request.form)
    return render_template('user_detail.html', user=user)

@app.route("/new_user_form")
def edit_new_user():
    return render_template('new_user_form.html')

@app.route("/add_user", methods=["POST"])
def create_new_user():
    user = User()

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    print(f"----->userid = {user.id}")
    db.session.commit() 
    print(f"after commit----->userid = {user.id}")

    return render_template('user_detail.html', user=user)

@app.route('/tags')
def list_tags():
    """Renders list of all tags"""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route("/tags/<tagid>")
def show_tag(tagid):
    tag = Tag.query.get(tagid)
    print(f"--look--->{tag.posts}")
    
    return render_template('show_tag.html', tag=tag)

@app.route("/tags/<tagid>/edit", methods=["POST"])
def edit_tag(tagid):
    """Handle request to Edit or delete tag, or cancel"""
    tag = Tag.query.get(tagid)
    which_button = request.form['edit_delete_cancel']
    if (which_button == 'Edit'):
        return render_template('edit_tag_form.html', tag=tag)
    elif (which_button == 'Delete'):
        ## Code to handle deletion of tag
        Tag.query.filter_by(id=tagid).delete()
        db.session.commit()
        tags = Tag.query.all()
        
        return render_template('tags.html', tags=tags)
    else: #cancel button
        tags = Tag.query.all()
        return render_template('tags.html', tags=tags)

@app.route("/save_tag", methods=["POST"])
def save_tag():
    which_button = request.form['save_cancel']
    if (which_button == "Save"):
        tagid = request.form['tagid']

        tag = Tag.query.get(tagid)

        #collect data from form
        tag.name = request.form['name']
        db.session.commit()
        #db.session.add(tag)
        return render_template('show_tag.html', tag=tag)
    else: # Cancel
        tags = Tag.query.all()
        return render_template('tags.html', tags=tags)

@app.route("/new_tag_form")
def edit_new_tag():
    return render_template('new_tag_form.html')

@app.route("/add_tag", methods=["POST"])
def create_new_tag():
    if (request.form['add_cancel'] == 'Add'):
        tag = Tag()

        tag.name = request.form['name']

        db.session.add(tag)
        db.session.commit() 

    return redirect("/users", code=302)


    

################### Blog Post methods #################

@app.route("/add_post_for_user/<userid>", methods=["POST"])
def edit_new_post(userid):
    """display the form to edit a new post for a given user"""
    user = User.query.get(userid)
    tags = Tag.query.all()
    return render_template('new_post.html', user=user, tags=tags)

@app.route("/add_post/<userid>", methods=["POST"])
def add_post(userid):
    user = User.query.get(userid)
    post = Post()
    post.title = request.form['title']
    post.content = request.form['content']
    post.userid = userid

    tags = [int(i) for i in request.form.getlist('chk_tag')]

    db.session.add(post) 
    db.session.commit() # need to commit new post before adding tags in order to get postid

    for tag_id in tags: 
        post_tag = PostTag()
        post_tag.post_id = post.id
        post_tag.tag_id = tag_id
            
        db.session.add(post_tag)

    db.session.commit() 
    return render_template('show_post.html', post=post)


@app.route("/posts/<postid>")
def show_post(postid):
    """Renders individual post detail page"""
    post = Post.query.get(postid)
    print (f"inside show_post, postid = {postid}")
    return render_template('show_post.html', post=post)

@app.route("/post_action/<postid>", methods=["POST"])
def post_action(postid):
    post = Post.query.get(postid)
    tags = Tag.query.all()
    selected_tags = PostTag.query.filter_by(post_id = postid).all()
    print(f"post_id = {postid}")
    print(f"----->selected_tags = {selected_tags}")
    sel_tags = []
    for pt in selected_tags:
        sel_tags.append(pt.tag_id)
        print(f"----->pt.tag_id")
        print(f"----->sel_tags = {sel_tags}")
    userid = post.userid
    which_button = request.form['cancel_edit_delete']
    print(f"----->Inside post_action, postid={postid}, request={which_button}")
    if (which_button == 'Edit'):
        return render_template('post_edit_form.html', post=post, tags=tags, selected_tags=sel_tags)
    elif which_button == "Delete":
        Post.query.filter_by(id=postid).delete()
        db.session.commit()
        return redirect(f"/users/{userid}", code=302)
    else: # Cancel button
        return redirect(f"/users/{userid}", code=302)

@app.route("/save_post/<postid>", methods=["POST"])
def post_save_cancel(postid):
    post = Post.query.get(postid)
    userid = post.userid
    which_button = request.form["add_cancel"]
    if (which_button == 'Save'):
        post.title = request.form['title']
        post.content = request.form['content']
        post.userid = userid
        tags = [int(i) for i in request.form.getlist('chk_tag')]
        print(f"tags = {tags}")
        post_tags = PostTag.query.filter_by(post_id=post.id)
        
        old_tag_ids = []
        for pt in post_tags:
            old_tag_ids.append(pt.tag_id)
        print(f"----->old_tag_ids = {old_tag_ids}")
        has_old_tags = False
        if len(old_tag_ids) > 0:
            has_old_tags = True
            #selected_tags = [int(j) for j in request.form.getlist('selected_tags')]
            #selected_tags = [int(j) for (j) in request.form['selected_tags']]
        
            selected_tags = request.form['selected_tags'].strip('][').split(', ')
            print(f"----->inside post_save_cancel, selected tags = {selected_tags}")
            #first, delete all unselected tags
            for selid in selected_tags:
                if selid not in old_tag_ids:
                    print(f"-----> try to delete <{selid}>")
                    PostTag.query.filter_by(tag_id=selid).delete()
                db.session.commit()

            else:
                print("----->No old tags found")

        for tag_id in tags: #if not selected before, but is now, add it. Otherwise ignore it.
            if (not has_old_tags or tag_id not in selected_tags):
                post_tag = PostTag()
                post_tag.post_id = postid
                post_tag.tag_id = tag_id
            
                db.session.add(post_tag)
        
            
        db.session.add(post)
        db.session.commit() 

        return render_template('show_post.html', post=post)
    else: #cancel
        return redirect(f"/users/{userid}", code=302) 
    


    