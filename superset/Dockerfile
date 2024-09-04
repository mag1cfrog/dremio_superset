FROM apache/superset:latest
# Switching to root to install the required packages
USER root


# COPY --chown=superset:superset entrypoint.sh /home/superset/entrypoint.sh
# RUN chmod +x /home/superset/entrypoint.sh

# Install Dremio SQLAlchemy Drivers
RUN pip install --no-cache-dir sqlalchemy sqlalchemy_dremio

# Execute the patch script
# RUN /bin/bash /home/superset/entrypoint.sh

COPY ./custom_dialect /home/superset/custom_dialect
ENV PYTHONPATH="${PYTHONPATH}:/home/superset"
RUN chmod +x /home/superset/custom_dialect/patch_dialect.py

# Copy the sitecustomize.py into the site-packages directory
COPY sitecustomize.py /usr/local/lib/python3.10/site-packages/sitecustomize.py

# Execute the patch to register the dialect
RUN python -m custom_dialect.patch_dialect

USER superset
ENV SUPERSET_SECRET_KEY=XgiVZQdtlIIeqUmo8Rs2d5hjuQZrXsJh
RUN superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email example@thisemailwillneverexist.xyz \
              --password admin
RUN superset db upgrade
# RUN superset load_examples
RUN superset init
