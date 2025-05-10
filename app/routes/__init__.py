from .fe_communication import fe_communication_bp

def register_routes(app):
    app.register_blueprint(fe_communication_bp)
