# main.py - Enhanced Multi-Platform Automation with Google Gemini AI
import requests
import json
import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
WEBHOOK_URL = os.environ.get('ZAPIER_WEBHOOK_URL', 'https://hooks.zapier.com/hooks/catch/17245945/u6zbdbj/')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

# Configure Gemini with the latest model
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Using the latest model
else:
    logger.warning("GEMINI_API_KEY not found. Using template-based generation as fallback.")
    model = None

class GeminiContentGenerator:
    def __init__(self):
        self.model = model
        
        # Platform-specific guidelines for AI prompts
        self.platform_guidelines = {
            "instagram": {
                "max_length": 2200,
                "optimal_length": 125,
                "style": "engaging, visual-focused, storytelling",
                "cta_required": True,
                "hashtag_limit": 30,
                "emojis": "encouraged"
            },
            "tiktok": {
                "max_length": 150,
                "optimal_length": 100,
                "style": "punchy, viral, trending",
                "cta_required": True,
                "hashtag_limit": 10,
                "emojis": "essential"
            },
            "twitter": {
                "max_length": 280,
                "optimal_length": 240,
                "style": "concise, witty, conversational",
                "cta_required": False,
                "hashtag_limit": 5,
                "emojis": "moderate"
            },
            "facebook": {
                "max_length": 63206,
                "optimal_length": 400,
                "style": "community-focused, detailed, personal",
                "cta_required": True,
                "hashtag_limit": 10,
                "emojis": "selective"
            },
            "linkedin": {
                "max_length": 3000,
                "optimal_length": 300,
                "style": "professional, industry-focused, educational",
                "cta_required": False,
                "hashtag_limit": 5,
                "emojis": "minimal"
            }
        }
        
        # Fallback templates if Gemini is unavailable
        self.fallback_templates = {
            "new-release": [
                "🎵 Just dropped something special! {context}. What do you think of this new direction? Let me know in the comments! 🔥",
                "New music alert! 🚨 {context} is finally here. This track means everything to me right now. Hope it resonates with you too! ✨"
            ],
            "studio-session": [
                "Late night studio vibes 🎛️ {context}. The creative process never stops, and tonight's session was pure magic. What fuels your creativity? 👇",
                "Back in the lab! {context}. Sometimes the best ideas come at the most unexpected times. Stay tuned for what's brewing! 🎶"
            ],
            "fan-appreciation": [
                "Y'all are incredible! 🙏 {context}. Your support keeps me going every single day. What's your favorite track right now? ❤️",
                "Feeling so grateful today 💫 {context}. This community we've built is everything. Thank you for being on this journey with me! 🌟"
            ],
            "behind-scenes": [
                "Behind the curtain 🎬 {context}. Not everything makes it to the final cut, but these moments are just as important. What would you like to see more of? 📸",
                "Raw creative moments 📹 {context}. The journey is just as beautiful as the destination. Share your creative process below! 💭"
            ]
        }
        
        # Genre-specific hashtag strategies  
        self.genre_hashtags = {
            "hip-hop": ["hiphop", "rap", "bars", "flow", "beats", "newrap", "undergroundhiphop"],
            "pop": ["popmusic", "newpop", "mainstream", "radio", "charts", "catchy", "newmusic"],
            "r&b": ["rnb", "soul", "smooth", "vocals", "rhythm", "newrnb", "soulmusic"],
            "indie": ["indiemusic", "independent", "alternative", "newartist", "undiscovered", "original"],
            "electronic": ["electronic", "edm", "synth", "beats", "dance", "producer", "newedm"],
            "rock": ["rockmusic", "guitar", "drums", "alternative", "newrock", "livemusic"]
        }
        
        self.universal_hashtags = ["newmusic", "artist", "musician", "music", "originalmusic", "songwriter", "producer"]
    
    def create_artist_profile(self, artist_id: str, stage_name: str, genre: str, brand_voice: str) -> Dict:
        """Create a comprehensive artist profile"""
        return {
            "artist_id": artist_id,
            "stage_name": stage_name,
            "genre": genre,
            "brand_voice": brand_voice,
            "platforms": ["instagram", "tiktok", "twitter", "facebook", "linkedin"],
            "hashtag_strategy": {
                platform: {
                    "brand": [f"{stage_name.lower().replace(' ', '')}music", f"{genre}artist"],
                    "genre": self.genre_hashtags.get(genre.lower(), ["music"])
                }
                for platform in ["instagram", "tiktok", "twitter", "facebook", "linkedin"]
            },
            "optimal_posting_times": {
                "instagram": "18:00",
                "tiktok": "19:00", 
                "twitter": "12:00",
                "facebook": "15:00",
                "linkedin": "09:00"
            }
        }
    
    def generate_ai_content(self, platform: str, theme: str, context: str, artist_profile: Dict) -> str:
        """Generate content using Google Gemini AI"""
        
        if not self.model:
            # Fallback to template-based generation
            return self._generate_fallback_content(theme, context, artist_profile["brand_voice"])
        
        try:
            guidelines = self.platform_guidelines[platform]
            
            # Construct detailed prompt for Gemini
            prompt = f"""
            Create a {platform} post for a {artist_profile['genre']} music artist named {artist_profile['stage_name']}.
            
            ARTIST PROFILE:
            - Name: {artist_profile['stage_name']}
            - Genre: {artist_profile['genre']}
            - Brand Voice: {artist_profile['brand_voice']} (adapt writing style accordingly)
            
            POST REQUIREMENTS:
            - Theme: {theme}
            - Context: {context}
            - Platform: {platform}
            - Style: {guidelines['style']}
            - Maximum Length: {guidelines['max_length']} characters
            - Optimal Length: {guidelines['optimal_length']} characters
            - {"Include a call-to-action" if guidelines['cta_required'] else "No call-to-action required"}
            - Emoji Usage: {guidelines['emojis']}
            
            BRAND VOICE GUIDELINES:
            - Energetic: Use exciting language, exclamation points, power words, create urgency and enthusiasm
            - Introspective: Be thoughtful, ask meaningful questions, share deeper insights, use contemplative tone
            - Rebellious: Challenge conventions, use bold statements, authentic raw expression, push boundaries
            - Playful: Include humor, wordplay, casual language, fun personality, lighthearted approach
            
            PLATFORM-SPECIFIC REQUIREMENTS:
            - Instagram: Visual storytelling, behind-the-scenes feel, community engagement
            - TikTok: Trend-aware, quick hooks, viral potential, youth-focused language
            - Twitter: Concise thoughts, conversational, real-time feel, newsworthy angle
            - Facebook: Community building, longer storytelling, personal connection
            - LinkedIn: Professional insights, industry perspective, career/business angle
            
            CONTENT THEMES:
            - new-release: Announce new music, build excitement, share the story behind the song
            - studio-session: Behind-the-scenes creative process, work-in-progress updates, artistic journey
            - fan-appreciation: Thank supporters, celebrate community, acknowledge audience impact
            - behind-scenes: Authentic moments, creative process, personal insights, vulnerability
            
            Generate ONLY the caption text. Do not include hashtags (they'll be added separately).
            Make it authentic to the artist's voice while optimized for {platform}'s audience and algorithm.
            """
            
            # Generate content with Gemini
            response = self.model.generate_content(prompt)
            generated_text = response.text.strip()
            
            # Validate and optimize length
            if len(generated_text) > guidelines['max_length']:
                # Truncate intelligently at sentence boundaries
                sentences = generated_text.split('.')
                truncated = ""
                for sentence in sentences:
                    if len(truncated + sentence + ".") <= guidelines['max_length'] - 10:
                        truncated += sentence + "."
                    else:
                        break
                generated_text = truncated.strip()
            
            logger.info(f"✅ Generated AI content for {artist_profile['stage_name']} on {platform}")
            return generated_text
            
        except Exception as e:
            logger.error(f"❌ Gemini AI generation failed: {e}. Using fallback.")
            return self._generate_fallback_content(theme, context, artist_profile["brand_voice"])
    
    def _generate_fallback_content(self, theme: str, context: str, brand_voice: str) -> str:
        """Fallback template-based generation if AI fails"""
        templates = self.fallback_templates.get(theme, ["Working on something special! {context} 🎵"])
        base_caption = random.choice(templates).format(context=context)
        
        # Apply brand voice adjustments
        if brand_voice == "energetic":
            base_caption = base_caption.replace(".", "!").replace("?", "?!")
        elif brand_voice == "introspective":
            base_caption = base_caption.replace("!", ".")
        elif brand_voice == "playful" and "😄" not in base_caption:
            base_caption += " 😄"
        
        return base_caption
    
    def generate_platform_hashtags(self, platform: str, artist_profile: Dict, theme: str) -> List[str]:
        """Generate strategic hashtags for each platform"""
        guidelines = self.platform_guidelines[platform]
        max_tags = guidelines["hashtag_limit"]
        
        hashtags = []
        
        # Add artist brand hashtags
        brand_tags = artist_profile["hashtag_strategy"][platform]["brand"]
        hashtags.extend(brand_tags[:2])
        
        # Add genre hashtags
        genre_tags = artist_profile["hashtag_strategy"][platform]["genre"]
        hashtags.extend(genre_tags[:3])
        
        # Add universal music hashtags
        hashtags.extend(self.universal_hashtags[:3])
        
        # Add theme-specific hashtags
        theme_tags = {
            "new-release": ["newrelease", "musicdrop", "freshmusic"],
            "studio-session": ["studio", "recording", "behindthescenes"],
            "fan-appreciation": ["grateful", "musicfamily", "blessed"],
            "behind-scenes": ["bts", "process", "journey"]
        }
        
        theme_specific = theme_tags.get(theme, ["music"])
        hashtags.extend(theme_specific[:2])
        
        # Remove duplicates and limit to platform maximum
        seen = set()
        unique_hashtags = []
        for tag in hashtags:
            if tag.lower() not in seen:
                seen.add(tag.lower())
                unique_hashtags.append(tag)
        
        return unique_hashtags[:max_tags]
    
    def send_to_zapier(self, content_data: Dict) -> bool:
        """Send generated content to Zapier webhook"""
        try:
            response = requests.post(WEBHOOK_URL, json=content_data, timeout=30)
            if response.status_code in [200, 201, 202]:
                logger.info(f"✅ Content sent to Zapier for {content_data['platform']}")
                return True
            else:
                logger.error(f"❌ Zapier webhook failed for {content_data['platform']}: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Error sending to Zapier for {content_data['platform']}: {e}")
            return False
    
    def create_multi_platform_campaign(self, artist_profile: Dict, theme: str, context: str) -> List[Dict]:
        """Generate AI-powered content for all platforms"""
        
        campaign_results = []
        
        logger.info(f"🤖 Generating AI content for {artist_profile['stage_name']} - {theme}")
        
        for platform in artist_profile["platforms"]:
            try:
                # Generate AI-powered content for this platform
                ai_caption = self.generate_ai_content(platform, theme, context, artist_profile)
                
                # Generate platform-optimized hashtags
                hashtags = self.generate_platform_hashtags(platform, artist_profile, theme)
                
                # Calculate optimal posting time
                base_time = datetime.now()
                optimal_time_str = artist_profile["optimal_posting_times"][platform]
                hour, minute = map(int, optimal_time_str.split(':'))
                posting_time = base_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                if posting_time <= base_time:
                    posting_time += timedelta(days=1)
                
                # Create webhook payload
                webhook_data = {
                    "content_id": f"{artist_profile['artist_id']}_{platform}_{theme}_{int(base_time.timestamp())}",
                    "artist_id": artist_profile["artist_id"],
                    "artist_name": artist_profile["stage_name"],
                    "platform": platform,
                    "caption": ai_caption,
                    "hashtags": hashtags,
                    "scheduled_time": posting_time.isoformat(),
                    "theme": theme,
                    "context": context,
                    "generation_method": "gemini_ai" if self.model else "template_fallback",
                    "generation_time": base_time.isoformat(),
                    "character_count": len(ai_caption),
                    "hashtag_count": len(hashtags),
                    "brand_voice": artist_profile["brand_voice"],
                    "genre": artist_profile["genre"]
                }
                
                # Send to Zapier
                success = self.send_to_zapier(webhook_data)
                
                campaign_results.append({
                    "platform": platform,
                    "success": success,
                    "caption": ai_caption[:100] + "..." if len(ai_caption) > 100 else ai_caption,
                    "hashtags": hashtags,
                    "posting_time": posting_time.isoformat(),
                    "character_count": len(ai_caption)
                })
                
                logger.info(f"{'✅' if success else '❌'} {platform.title()}: {ai_caption[:50]}...")
                
            except Exception as e:
                logger.error(f"❌ Failed to create content for {platform}: {e}")
                campaign_results.append({
                    "platform": platform,
                    "success": False,
                    "error": str(e)
                })
        
        return campaign_results

def create_sample_artists():
    """Create sample artist profiles for AI content generation"""
    generator = GeminiContentGenerator()
    
    artists = [
        generator.create_artist_profile("alex_rivers", "Alex Rivers", "indie", "introspective"),
        generator.create_artist_profile("maya_sound", "Maya Sound", "pop", "energetic"),
        generator.create_artist_profile("echo_beats", "Echo Beats", "electronic", "rebellious"),
        generator.create_artist_profile("soul_voice", "Soul Voice", "r&b", "playful")
    ]
    
    return artists

def run_ai_content_campaign():
    """Generate AI-powered content for all artists across all platforms"""
    logger.info("🚀 Starting AI-powered multi-platform campaign...")
    
    if not GEMINI_API_KEY:
        logger.warning("⚠️ GEMINI_API_KEY not set. Using template fallback mode.")
    else:
        logger.info("🤖 Gemini AI configured and ready!")
    
    generator = GeminiContentGenerator()
    artists = create_sample_artists()
    
    # Varied content themes for more diverse posting
    themes = ["new-release", "studio-session", "fan-appreciation", "behind-scenes"]
    
    # Rich context examples for AI to work with
    context_examples = {
        "new-release": [
            "my latest single 'Midnight Dreams' featuring ethereal vocals and atmospheric production",
            "this emotional ballad I wrote during quarantine about finding hope in darkness",
            "an upbeat anthem about self-discovery and breaking free from limitations"
        ],
        "studio-session": [
            "late night recording session experimenting with vintage analog equipment",
            "collaborating with a Grammy-winning producer on my upcoming EP",
            "layering harmonies and perfecting the bridge section of my next hit"
        ],
        "fan-appreciation": [
            "reaching 10K monthly listeners on Spotify thanks to your incredible support",
            "seeing fans sing along to my songs at last weekend's intimate acoustic show",
            "receiving heartfelt messages about how my music helped people through tough times"
        ],
        "behind-scenes": [
            "the creative process behind my latest music video shoot in downtown LA",
            "songwriting inspiration from a 3am walk through the city streets",
            "the story behind the cryptic lyrics in my most personal song yet"
        ]
    }
    
    total_posts = 0
    successful_posts = 0
    
    for artist in artists:
        theme = random.choice(themes)
        context = random.choice(context_examples[theme])
        
        logger.info(f"\n🎵 Creating AI campaign for {artist['stage_name']} - {theme}")
        logger.info(f"📝 Context: {context}")
        
        # Generate AI content for all platforms
        results = generator.create_multi_platform_campaign(artist, theme, context)
        
        # Log results
        for result in results:
            total_posts += 1
            if result["success"]:
                successful_posts += 1
                logger.info(f"  📱 {result['platform']}: {result['character_count']} chars, {len(result['hashtags'])} hashtags")
    
    logger.info(f"\n🎉 AI Campaign complete!")
    logger.info(f"📊 Success rate: {successful_posts}/{total_posts} posts")
    logger.info(f"🤖 Generation method: {'Gemini AI' if GEMINI_API_KEY else 'Template Fallback'}")
    logger.info(f"📱 Platforms: Instagram, TikTok, Twitter, Facebook, LinkedIn")
    
    return successful_posts, total_posts

def test_ai_generation():
    """Test AI content generation for a single artist/platform"""
    logger.info("🧪 Testing AI content generation...")
    
    generator = GeminiContentGenerator()
    artist = generator.create_artist_profile("test_artist", "Test Artist", "pop", "energetic")
    
    # Test different platforms
    platforms = ["instagram", "tiktok", "twitter"]
    
    for platform in platforms:
        print(f"\n--- {platform.title()} Test ---")
        content = generator.generate_ai_content(
            platform, 
            "new-release", 
            "my debut single 'Electric Dreams' with a futuristic synth-pop sound",
            artist
        )
        hashtags = generator.generate_platform_hashtags(platform, artist, "new-release")
        
        print(f"Caption ({len(content)} chars): {content}")
        print(f"Hashtags: {' '.join(['#' + tag for tag in hashtags])}")
    
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_ai_generation()
    else:
        run_ai_content_campaign()
