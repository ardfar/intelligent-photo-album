from flask import Flask, jsonify, render_template, request, redirect, url_for, send_file
import tqdm
import time

import classes.AppConfig as AppConfig
import classes.Inference as Inference
import classes.Folder as Folder
import classes.Hashtag as Hashtag
import classes.Search as Search
import classes.Index as Index
import classes.Photo as Photo
import classes.Album as Album

app = Flask(__name__)
AppConfig = AppConfig.AppConfig()
Infer = Inference.Inference()
Index = Index.Index()

def get_objects_album(unique_objects = Index.get_unique_objects(),limit=8):
    Objects = []
    for obj in unique_objects[:limit]:
        object = Album.Album(obj, 'object') 
        object.get_members()
        
        Objects.append(object)
        
    return Objects

def get_folders_album(unique_folder = AppConfig.read_config()["folders"],limit=8):
    Folders = []
    for folder in unique_folder[:limit]:
        fld = Album.Album(folder, 'folder') 
        fld.get_members()
        
        Folders.append(fld)
        
    return Folders

def get_types_album(unique_types = Index.get_unique_types(), limit=8):
    Types = []
    for typ in unique_types[:limit]:
        type = Album.Album(typ, 'type')
        type.get_members()
            
        Types.append(type) 
        
    return Types[:limit]

@app.route('/get_image/<image_path>')
def get_image(image_path):
    return send_file(image_path, mimetype='image/jpg')

@app.route('/get_caption/<image_path>')
def get_caption(image_path):
    config = AppConfig.read_config()
   
    
    if config['inference']['option']['caption_generation']:
        image_data = Photo.Photo(image_path)
        image_data.load_image_from_index()
        caption = image_data.caption
    else:
        caption = Infer.get_caption(image_path)
    
    return caption

@app.route('/get_hashtags/<type>/<caption>')
def get_hashtag(type, caption):
    hashtags = ["#"+type]
    
    hashtags.append(Hashtag.Hashtag.generate_hashtags(type)["data"]["results"][:3])
    
    for entity in Infer.get_entities(caption):
        hashtags.append("#"+entity)
        hashtags.append(Hashtag.Hashtag.generate_hashtags(entity)["data"]["results"][:3])
    
    
    return hashtags

@app.route('/')
def index():
    Objects = get_objects_album()
    Types = get_types_album()
    Folders = get_folders_album()
    return render_template('index.html', objects=Objects, types=Types, folders=Folders)

@app.route('/config')
def configuration():
    config = AppConfig.read_config()
    
    folders = config['folders']
    folder_info = []
    for folder in folders:
        folder = Folder.Folder(folder)
        num_images = folder.count_images()
        info = {'path': folder.path, 'num_images': num_images}
        folder_info.append(info)
        
    infer_config = config['inference']
    
    return render_template('configuration.html', folders=folder_info, infer_config=infer_config)

@app.route('/category/<category>')
def category(category):
    if category == 'object':
        albums = get_objects_album(limit=100)
    elif category == 'folder':
        albums = get_folders_album(limit=100)
    else:
        albums = get_types_album(limit=100)
    return render_template('category.html', category=category ,albums=albums)

@app.route('/album/<type>/<name>')
def album(name, type):
    album = Album.Album(name, type)
    album.get_members()
    
    return render_template('album.html', album=album ,type=type)

@app.route('/search', methods=['POST'])
def search():
    query = request.form['search']
    
    results = Search.Search(query).get_members()
    
    print(results["rObject"])
    
    return render_template('search.html', results=results, query=query)

@app.route('/update-configuration', methods=['POST']) 
def update_config():
    config = AppConfig.read_config()
    infer_config = config['inference']
    
    infer_opt = infer_config['option']
    
    obj_det = request.form['obj_det']
    scn_cls = request.form['scn_cls']
    ocr_scn = request.form['ocr_scn']
    cap_gen = request.form['cap_gen']
    
    infer_opt['object_detection'] = True if obj_det == 'True' else False
    infer_opt['scene_classification'] = True if scn_cls == 'True' else False
    infer_opt['ocr'] = True if ocr_scn == 'True' else False
    infer_opt['caption_generation'] = True if cap_gen == 'True' else False
    
    config['inference']['option'] = infer_opt
    
    print(config)
    
    AppConfig.write_config(config)
    
    return redirect(url_for('configuration'))

@app.route('/add-folder', methods=['POST']) 
def add_folder():
    config = AppConfig.read_config()
    folder = request.form['folder_input']
    config['folders'].append(folder)
    
    AppConfig.write_config(config)
    
    return redirect(url_for('configuration'))

@app.route('/remove-folder', methods=['POST']) 
def remove_folder():
    config = AppConfig.read_config()
    folder = request.form['folder_input']
    config['folders'].remove(folder)
    
    AppConfig.write_config(config)
    
    return redirect(url_for('configuration'))

@app.route('/re-index')
def re_index():
    config = AppConfig.read_config()
    Index.reset_index()
    length = 0
    
    start_time = time.time()

    for folder in config['folders']:
        folder = Folder.Folder(folder)
        images = tqdm.tqdm(folder.get_images())
        images.set_description(folder.path)
        
        length += len(images)
        
        for image in images:
            photo = Photo.Photo(image)
            
            if config['inference']['option']['object_detection']:
                photo.set_objects(Infer.get_objects(image))
            
            if config['inference']['option']['ocr']:
                photo.set_text(Infer.get_text(image))
            
            if config['inference']['option']['scene_classification']:
                photo.set_class(Infer.get_scene(image))
                
            if config['inference']['option']['caption_generation']:
                photo.set_caption(Infer.get_caption(image))
            
            photo.save()

    end_time = time.time()
    execution_time = end_time - start_time
    
    return jsonify({'status': 'success', 'time': execution_time, 'length': length})

if __name__ == '__main__':
    app.run(debug=True)