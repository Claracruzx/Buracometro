# Deploy do Buracometro na Vercel

Na Vercel, use estas configuracoes:

- Framework Preset: Other
- Root Directory: vazio
- Build Command: `python manage.py collectstatic --noinput`
- Output Directory: vazio

## Variaveis de ambiente

Cadastre em Project Settings > Environment Variables:

```env
DEBUG=False
SECRET_KEY=uma-chave-secreta-grande-e-unica
ALLOWED_HOSTS=.vercel.app
CSRF_TRUSTED_ORIGINS=https://*.vercel.app
DATABASE_URL=postgres://usuario:senha@host:5432/banco
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=0
```

Depois do primeiro deploy, rode as migrations no banco online:

```bash
python manage.py migrate
```

E crie um admin:

```bash
python manage.py createsuperuser
```
