from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firestore
cred = credentials.Certificate("sbh25-2d8ba-firebase-adminsdk-fbsvc-d4cce1ee41.json")  # Update with your credentials
firebase_admin.initialize_app(cred)
db = firestore.client()

# Fetch all products from a specific branch of a provider
@app.route('/get_products/<provider>/<branch>', methods=['GET'])
def get_products(provider_name, branch):
    products_ref = db.collection("provider").document(provider_name).collection(branch)
    docs = products_ref.stream()
    products = {doc.id: doc.to_dict() for doc in docs}
    
    if products:
        return jsonify(products)
    else:
        return jsonify({"error": "No products found"}), 404

# Fetch product location from a specific branch
@app.route('/get_location/<provider>/<branch>', methods=['GET'])
def get_location(provider, branch):
    doc_ref = db.collection("provider").document(provider).collection(branch).document("location")
    doc = doc_ref.get()

    if doc.exists:
        return jsonify(doc.to_dict())
    else:
        return jsonify({"error": "Location data not found"}), 404


# Get Retailers Option
@app.route('/get_providers', methods=['GET'])
def get_providers():
    providers_ref = db.collection('provider')
    docs = providers_ref.stream()

    provider_list = [doc.id for doc in docs]  # Get document IDs as options

    return jsonify(provider_list)

# Fetch all branches for a selected provider
@app.route('/get_branches/<provider>', methods=['GET'])
def get_branches(provider):
    try:
        # Reference to the provider document
        provider_doc = db.collection('provider').document(provider)
        
        # Get all subcollections (branches) under the selected provider
        branches = provider_doc.collections()
        
        # Extract collection names
        branch_list = [branch.id for branch in branches]  

        if not branch_list:
            return jsonify({"error": "No branches found"}), 404

        return jsonify(branch_list)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
