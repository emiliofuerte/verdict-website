from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image
import os

class Command(BaseCommand):
    help = 'Compress all images in the media folder'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quality',
            type=int,
            default=85,
            help='JPEG quality (1-100, default: 85)',
        )
        parser.add_argument(
            '--max-width',
            type=int,
            default=1200,
            help='Maximum width in pixels (default: 1200)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be compressed without actually doing it',
        )

    def handle(self, *args, **options):
        quality = options['quality']
        max_width = options['max_width']
        dry_run = options['dry_run']

        media_root = settings.MEDIA_ROOT
        total_saved = 0
        files_processed = 0

        for root, dirs, files in os.walk(media_root):
            for filename in files:
                if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue

                filepath = os.path.join(root, filename)
                original_size = os.path.getsize(filepath)

                try:
                    with Image.open(filepath) as img:
                        # Convert RGBA to RGB for JPEGs
                        if img.mode in ('RGBA', 'LA', 'P'):
                            background = Image.new('RGB', img.size, (255, 255, 255))
                            if img.mode == 'P':
                                img = img.convert('RGBA')
                            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                            img = background

                        # Resize if too large
                        if img.width > max_width:
                            ratio = max_width / img.width
                            new_height = int(img.height * ratio)
                            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

                        if dry_run:
                            self.stdout.write(f"Would compress: {filepath}")
                            continue

                        # Save with compression
                        img.save(filepath, 'JPEG', quality=quality, optimize=True)

                    new_size = os.path.getsize(filepath)
                    saved = original_size - new_size
                    total_saved += saved
                    files_processed += 1

                    percent_saved = (saved / original_size * 100) if original_size > 0 else 0
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ {filename}: {original_size//1024}KB → {new_size//1024}KB "
                            f"(saved {percent_saved:.1f}%)"
                        )
                    )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"✗ Failed to compress {filename}: {e}")
                    )

        if dry_run:
            self.stdout.write(self.style.WARNING("\nDry run complete. No files were modified."))
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✓ Compressed {files_processed} images, "
                    f"saved {total_saved//1024}KB total"
                )
            )
