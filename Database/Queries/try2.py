from flask import Flask, jsonify
import pyodbc

app = Flask(__name__)


def get_db_connection():
    try:
        conn = pyodbc.connect('your_connection_string')
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to database: {e}")
        return None


@app.route('/categories', methods=['GET'])
def get_categories():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT CategoryName FROM Categories")
        categories = [row.CategoryName for row in cursor.fetchall()]
        print(categories)
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)



extractor = StyleContentModel(style_layers, content_layers)
style_targets = extractor(style_image)['style']
content_targets = extractor(content_image)['content']
image = tf.Variable(content_image)

def clip_0_1(image):
  return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)

opt = tf.keras.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)

style_weight=1e-2
content_weight=1e4

def style_content_loss(outputs):
  style_outputs = outputs['style']
  content_outputs = outputs['content']
  style_loss = tf.add_n([tf.reduce_mean((style_outputs[name]-style_targets[name])**2) for name in style_outputs.keys()])
  style_loss *= style_weight / num_style_layers
  content_loss = tf.add_n([tf.reduce_mean((content_outputs[name]-content_targets[name])**2) for name in content_outputs.keys()])
  content_loss *= content_weight / num_content_layers
  loss = style_loss + content_loss
  return loss
