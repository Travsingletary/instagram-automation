# main.py - Multi-Platform Social Media Automation for Lovable/Render
import requests
import json
import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get webhook URL from environment variable
WEBHOOK_URL = os.environ.get('ZAPIER_WEBHOOK_URL', 'https://hooks.zapier.com/hooks/catch/17245945/u6zbdbj/')

class MultiPlatformContentGenerator:
    def __init__(self):
        # Platform-specific content templates optimized for each social network
        self.platform_templates = {
            "instagram": {
                "new-release": [
                    "🎵 Just dropped something special for you all! {context}. What do you hear when you listen? Drop a comment and let me know which part hits different for you! 🔥\n\nStream it now - link in bio!",
                    "New music alert! 🚨 {context} is finally here and I'm beyond excited to share this with you. This track represents exactly where I am right now as an artist.\n\nWhat's your first impression? Let me know! 🎶"
                ],
                "studio-session": [
                    "Late night studio vibes hitting different ✨ {context}. Sometimes the magic happens when you least expect it.\n\nThis is where the real work happens - behind the scenes, finding that perfect sound.\n\nWhat's your creative space look like? Show me! 👇"
                ],
                "fan-appreciation": [
                    "Y'all are absolutely incredible 🙏 {context}. Seeing your support, hearing you connect with the music - this is why I do what I do.\n\nYou're not just fans, you're family. What's your favorite track right now? ❤️"
                ]
            },
            "tiktok": {
                "new-release": [
                    "POV: You just dropped your best track yet 🎵 {context} #NewMusic #MusicTok #ArtistLife",
                    "When the song you've been working on for months finally drops... {context} ✨ #MusicProducer #NewRelease #Viral"
                ],
                "studio-session": [
                    "Studio sessions at 3am hit different 🎛️ {context} #StudioLife #MusicMaking #BehindTheScenes #Producer",
                    "When inspiration strikes in the studio... {context} 🔥 #MusicProcess #Recording #Creative"
                ],
                "fan-appreciation": [
                    "Y'all really said 'we see you' 🥺 {context} #Grateful #MusicFamily #Blessed #Artist",
                    "The support has been UNREAL lately 💫 {context} #ThankYou #MusicCommunity #Love"
                ]
            },
            "twitter": {
                "new-release": [
                    "🎵 NEW MUSIC OUT NOW! {context} - this one's been brewing for a while and I'm finally ready to share it with the world. What do you think?",
                    "JUST DROPPED: {context} 🚨 Been working on this for months. Hope it hits as hard for you as it does for me 🔥"
                ],
                "studio-session": [
                    "4am studio sessions are where the magic happens ✨ {context} #StudioLife",
                    "Currently: {context} and questioning all my life choices but in the best way 😅 #MusicProducer"
                ],
                "fan-appreciation": [
                    "Still can't believe the support lately 🙏 {context} - you all are the reason I keep creating",
                    "Grateful is an understatement 💜 {context} #MusicFamily"
                ]
            },
            "facebook": {
                "new-release": [
                    "I'm excited to share my latest track with you all! {context}. This song has been a labor of love, and I can't wait for you to experience the journey it takes you on.\n\nMusic has always been my way of connecting with people, and this track is no exception. Let me know what you think in the comments!",
                    "New music is here! 🎵 {context} represents a new chapter in my artistic journey. I've poured my heart into every note, every lyric, every beat.\n\nThank you for being part of this incredible journey with me. Your support means everything."
                ],
                "studio-session": [
                    "Taking you behind the scenes today! {context}. There's something magical about the creative process - those late nights, the moments of inspiration, the challenges that push you to grow as an artist.\n\nWhat does your creative process look like? I'd love to hear about it!",
                    "Studio life update: {context}. The creative process is never linear, but that's what makes it beautiful. Every session brings new discoveries, new sounds, new possibilities."
                ],
                "fan-appreciation": [
                    "I want to take a moment to express my genuine gratitude. {context}. Every like, every share, every comment - it all matters more than you know.\n\nMusic is meant to be shared, and having a community like this makes every song worth creating. Thank you for being part of this journey.",
                    "Feeling incredibly blessed today. {context}. This community we've built together is something special, and I don't take it for granted.\n\nYour support not only helps me as an artist but inspires me to keep pushing boundaries and creating music that matters."
                ]
            },
            "linkedin": {
                "new-release": [
                    "Excited to share my latest music release! {context}. As an independent artist, every release is both a creative milestone and a business achievement.\n\nThe music industry continues to evolve, and I'm grateful for platforms that allow artists to connect directly with their audience. #MusicBusiness #IndependentArtist",
                    "New music is live! {context}. Behind every song is months of creative work, collaboration, and strategic planning.\n\nFor fellow creatives and entrepreneurs: what's your approach to launching new projects? #CreativeEntrepreneur #MusicIndustry"
                ],
                "studio-session": [
                    "Behind the scenes of music production: {context}. The creative process requires both artistic vision and technical execution.\n\nEvery studio session is a lesson in project management, creative problem-solving, and collaboration. #MusicProduction #CreativeProcess",
                    "Studio insights: {context}. Building a music career involves constant learning and adaptation.\n\nThe intersection of creativity and technology continues to shape how we create and share music. #MusicTech #Innovation"
                ],
                "fan-appreciation": [
                    "Reflecting on recent milestones: {context}. Building a sustainable music career is only possible with genuine community support.\n\nGrateful for everyone who has been part of this journey - from industry professionals to dedicated listeners. #MusicCommunity #Entrepreneurship",
                    "Community update: {context}. Success in the creative industries is built on authentic relationships and consistent value creation.\n\nThank you to everyone who continues to support independent artistry. #IndependentArtist #Community"
                ]
            }
        }
        
        # Platform-specific hashtag strategies
        self.platform_hashtags = {
            "instagram": {
                "base": ["music", "artist", "musician", "newmusic", "songwriter", "producer"],
                "genre_tags": {
                    "hip-hop": ["hiphop", "rap", "bars", "flow", "beats", "newrap"],
                    "pop": ["popmusic", "newpop", "mainstream", "catchy", "radio"],
                    "r&b": ["rnb", "soul", "smooth", "vocals", "rhythm"],
                    "indie": ["indiemusic", "independent", "alternative", "newartist"],
                    "electronic": ["electronic", "edm", "synth", "producer", "beats"],
                    "rock": ["rockmusic", "guitar", "alternative", "livemusic"]
                }
            },
            "tiktok": {
                "base": ["music", "musictok", "artist", "newmusic", "viral", "fyp"],
                "genre_tags": {
                    "hip-hop": ["hiphoptok", "rap", "bars", "flow", "beats"],
                    "pop": ["poptok", "popmusic", "catchy", "mainstream"],
                    "r&b": ["rnbtok", "soul", "vocals", "smooth"],
                    "indie": ["indietok", "independent", "alternative"],
                    "electronic": ["edm", "electronictok", "synth", "producer"],
                    "rock": ["rocktok", "guitar", "alternative"]
                }
            },
            "twitter": {
                "base": ["Music", "NewMusic", "Artist", "Musician"],
                "genre_tags": {
                    "hip-hop": ["HipHop", "Rap", "Beats"],
                    "pop": ["PopMusic", "Pop"],
                    "r&b": ["RnB", "Soul"],
                    "indie": ["IndieMusic", "Independent"],
                    "electronic": ["Electronic", "EDM"],
                    "rock": ["Rock", "Guitar"]
                }
            },
            "facebook": {
                "base": ["music", "newmusic", "artist"],
                "genre_tags": {
                    "hip-hop": ["hiphop", "rap"],
                    "pop": ["pop", "popmusic"],
                    "r&b": ["rnb", "soul"],
                    "indie": ["indie", "independent"],
                    "electronic": ["electronic", "edm"],
                    "rock": ["rock", "livemusic"]
                }
            },
            "linkedin": {
                "base": ["Music", "CreativeIndustry", "MusicBusiness", "IndependentArtist"],
                "genre_tags": {
                    "hip-hop": ["HipHop", "MusicProduction"],
                    "pop": ["PopMusic", "MusicIndustry"],
                    "r&b": ["RnB", "SoulMusic"],
                    "indie": ["IndieMusic", "CreativeEntrepreneur"],
                    "electronic": ["ElectronicMusic", "MusicTech"],
                    "rock": ["RockMusic", "LiveMusic"]
                }
            }
        }
        
        # Platform-specific character limits and optimization
        self.platform_specs = {
            "instagram": {"max_caption": 2200, "optimal_caption": 125, "max_hashtags": 30},
            "tiktok": {"max_caption": 150, "optimal_caption": 100, "max_hashtags": 10},
            "twitter": {"max_caption": 280, "optimal_caption": 240, "max_hashtags": 5},
            "facebook": {"max_caption": 63206, "optimal_caption": 400, "max_hashtags": 10},
            "linkedin": {"max_caption": 3000, "optimal_caption": 300, "max_hashtags": 5}
        }
    
    def create_artist_profile(self, artist_id: str, stage_name: str, genre: str, brand_voice: str) -> Dict:
        """Create a comprehensive artist profile for multi-platform posting"""
        return {
            "artist_id": artist_id,
            "stage_name": stage_name,
            "genre": genre,
            "brand_voice": brand_voice,
            "platforms": ["instagram", "tiktok", "twitter", "facebook", "linkedin"],  # All Buffer-supported platforms
            "hashtag_strategy": {
                platform: {
                    "brand": [f"{stage_name.lower().replace(' ', '')}music", f"{genre}artist"],
                    "genre": self.platform_hashtags[platform]["genre_tags"].get(genre.lower(), ["music"])
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
    
    def generate_platform_content(self, platform: str, theme: str, context: str, artist_profile: Dict) -> Dict:
        """Generate content optimized for a specific platform"""
        
        # Get platform-specific template
        templates = self.platform_templates[platform].get(theme, [f"Working on something special! {context}"])
        base_caption = random.choice(templates).format(context=context)
        
        # Apply brand voice adjustments
        caption = self.apply_brand_voice(base_caption, artist_profile["brand_voice"], platform)
        
        # Generate platform-optimized hashtags
        hashtags = self.generate_platform_hashtags(platform, artist_profile, theme)
        
        # Apply platform-specific optimization
        optimized_caption = self.optimize_for_platform(caption, platform)
        
        return {
            "platform": platform,
            "caption": optimized_caption,
            "hashtags": hashtags,
            "character_count": len(optimized_caption),
            "hashtag_count": len(hashtags)
        }
    
    def apply_brand_voice(self, caption: str, brand_voice: str, platform: str) -> str:
        """Apply artist's brand voice with platform considerations"""
        
        voice_adjustments = {
            "energetic": {
                "instagram": lambda c: c.replace(".", "!").replace("?", "?!"),
                "tiktok": lambda c: c.upper() if len(c) < 50 else c.replace(".", "!"),
                "twitter": lambda c: c.replace("amazing", "AMAZING").replace("incredible", "INCREDIBLE"),
                "facebook": lambda c: c.replace(".", "!"),
                "linkedin": lambda c: c.replace("excited", "thrilled")
            },
            "introspective": {
                "instagram": lambda c: c.replace("!", "."),
                "tiktok": lambda c: c.replace("!", "..."),
                "twitter": lambda c: c.lower().replace("!", "."),
                "facebook": lambda c: c,
                "linkedin": lambda c: c.replace("feel", "reflect on")
            },
            "rebellious": {
                "instagram": lambda c: c.replace("amazing", "wild").replace("incredible", "insane"),
                "tiktok": lambda c: c.replace("good", "fire").replace("great", "sick"),
                "twitter": lambda c: c.replace("nice", "dope"),
                "facebook": lambda c: c.replace("traditional", "conventional"),
                "linkedin": lambda c: c.replace("different", "innovative")
            },
            "playful": {
                "instagram": lambda c: c + " 😄" if "😄" not in c else c,
                "tiktok": lambda c: c + " 😂" if "😂" not in c else c,
                "twitter": lambda c: c + " 😊" if "😊" not in c else c,
                "facebook": lambda c: c + " 🙂" if "🙂" not in c else c,
                "linkedin": lambda c: c + " 😊" if "😊" not in c else c
            }
        }
        
        platform_adjustment = voice_adjustments.get(brand_voice, {}).get(platform)
        return platform_adjustment(caption) if platform_adjustment else caption
    
    def generate_platform_hashtags(self, platform: str, artist_profile: Dict, theme: str) -> List[str]:
        """Generate hashtags optimized for specific platform"""
        
        hashtags = []
        max_tags = self.platform_specs[platform]["max_hashtags"]
        
        # Add artist brand hashtags
        brand_tags = artist_profile["hashtag_strategy"][platform]["brand"]
        hashtags.extend(brand_tags[:2])
        
        # Add genre hashtags
        genre_tags = artist_profile["hashtag_strategy"][platform]["genre"]
        hashtags.extend(genre_tags[:3])
        
        # Add platform base hashtags
        base_tags = self.platform_hashtags[platform]["base"]
        hashtags.extend(base_tags[:3])
        
        # Add theme-specific hashtags
        theme_tags = {
            "new-release": {
                "instagram": ["newrelease", "musicdrop", "freshmusic"],
                "tiktok": ["newmusic", "musicdrop", "viral"],
                "twitter": ["NewMusic", "MusicDrop"],
                "facebook": ["newrelease", "music"],
                "linkedin": ["NewRelease", "MusicLaunch"]
            },
            "studio-session": {
                "instagram": ["studio", "recording", "behindthescenes"],
                "tiktok": ["studiolife", "musicmaking", "bts"],
                "twitter": ["Studio", "Recording"],
                "facebook": ["studio", "musicmaking"],
                "linkedin": ["StudioWork", "MusicProduction"]
            },
            "fan-appreciation": {
                "instagram": ["grateful", "musicfamily", "blessed"],
                "tiktok": ["grateful", "thankful", "love"],
                "twitter": ["Grateful", "ThankYou"],
                "facebook": ["grateful", "community"],
                "linkedin": ["Grateful", "Community"]
            }
        }
        
        theme_specific = theme_tags.get(theme, {}).get(platform, ["music"])
        hashtags.extend(theme_specific[:2])
        
        # Remove duplicates and limit to platform max
        seen = set()
        unique_hashtags = []
        for tag in hashtags:
            if tag.lower() not in seen:
                seen.add(tag.lower())
                unique_hashtags.append(tag)
        
        return unique_hashtags[:max_tags]
    
    def optimize_for_platform(self, caption: str, platform: str) -> str:
        """Apply platform-specific optimization"""
        
        specs = self.platform_specs[platform]
        
        # Truncate if too long
        if len(caption) > specs["max_caption"]:
            caption = caption[:specs["max_caption"]-3] + "..."
        
        # Platform-specific formatting
        if platform == "twitter":
            # Remove excessive line breaks for Twitter
            caption = caption.replace('\n\n', '\n')
        elif platform == "linkedin":
            # Add professional spacing for LinkedIn
            caption = caption.replace('\n', '\n\n')
        elif platform == "tiktok":
            # Keep it concise and punchy for TikTok
            if len(caption) > specs["optimal_caption"]:
                sentences = caption.split('.')
                caption = sentences[0] + "."
        
        return caption
    
    def send_to_zapier(self, content_data: Dict) -> bool:
        """Send generated content to Zapier webhook"""
        try:
            response = requests.post(WEBHOOK_URL, json=content_data, timeout=30)
            if response.status_code in [200, 201, 202]:
                logger.info(f"✅ Content sent to Zapier successfully for {content_data['platform']}")
                return True
            else:
                logger.error(f"❌ Zapier webhook failed for {content_data['platform']}: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Error sending to Zapier for {content_data['platform']}: {e}")
            return False
    
    def create_multi_platform_campaign(self, artist_profile: Dict, theme: str, context: str) -> List[Dict]:
        """Generate content for all platforms and send to Zapier"""
        
        campaign_results = []
        
        for platform in artist_profile["platforms"]:
            try:
                # Generate platform-specific content
                platform_content = self.generate_platform_content(platform, theme, context, artist_profile)
                
                # Calculate optimal posting time for this platform
                base_time = datetime.now()
                optimal_time_str = artist_profile["optimal_posting_times"][platform]
                hour, minute = map(int, optimal_time_str.split(':'))
                posting_time = base_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                if posting_time <= base_time:
                    posting_time += timedelta(days=1)
                
                # Create comprehensive webhook payload
                webhook_data = {
                    "content_id": f"{artist_profile['artist_id']}_{platform}_{theme}_{int(base_time.timestamp())}",
                    "artist_id": artist_profile["artist_id"],
                    "artist_name": artist_profile["stage_name"],
                    "platform": platform,
                    "caption": platform_content["caption"],
                    "hashtags": platform_content["hashtags"],
                    "scheduled_time": posting_time.isoformat(),
                    "theme": theme,
                    "context": context,
                    "generation_time": base_time.isoformat(),
                    "character_count": platform_content["character_count"],
                    "hashtag_count": platform_content["hashtag_count"],
                    "brand_voice": artist_profile["brand_voice"],
                    "genre": artist_profile["genre"]
                }
                
                # Send to Zapier
                success = self.send_to_zapier(webhook_data)
                
                campaign_results.append({
                    "platform": platform,
                    "success": success,
                    "content": platform_content,
                    "posting_time": posting_time.isoformat()
                })
                
                logger.info(f"{'✅' if success else '❌'} {platform.title()}: {platform_content['caption'][:50]}...")
                
            except Exception as e:
                logger.error(f"❌ Failed to create content for {platform}: {e}")
                campaign_results.append({
                    "platform": platform,
                    "success": False,
                    "error": str(e)
                })
        
        return campaign_results

def create_sample_artists():
    """Create sample artist profiles for multi-platform posting"""
    generator = MultiPlatformContentGenerator()
    
    artists = [
        generator.create_artist_profile("alex_rivers", "Alex Rivers", "indie", "introspective"),
        generator.create_artist_profile("maya_sound", "Maya Sound", "pop", "energetic"),
        generator.create_artist_profile("echo_beats", "Echo Beats", "electronic", "rebellious"),
        generator.create_artist_profile("soul_voice", "Soul Voice", "r&b", "playful")
    ]
    
    return artists

def run_daily_multi_platform_campaign():
    """Generate and post content across all platforms for all artists"""
    logger.info("🚀 Starting daily multi-platform campaign...")
    
    generator = MultiPlatformContentGenerator()
    artists = create_sample_artists()
    
    # Rotate through different themes
    themes = ["new-release", "studio-session", "fan-appreciation", "behind-scenes"]
    
    # Context examples for variety
    context_examples = {
        "new-release": ["my latest single", "this new track I've been working on", "something special I just finished"],
        "studio-session": ["late night recording", "new material in progress", "experimenting with fresh sounds"],
        "fan-appreciation": ["reaching 5K followers", "incredible support lately", "amazing response to my music"],
        "behind-scenes": ["my songwriting process", "studio setup tour", "creative journey updates"]
    }
    
    total_posts = 0
    successful_posts = 0
    
    for artist in artists:
        theme = random.choice(themes)
        context = random.choice(context_examples[theme])
        
        logger.info(f"\n🎵 Creating campaign for {artist['stage_name']} - {theme}")
        
        # Create content for all platforms
        results = generator.create_multi_platform_campaign(artist, theme, context)
        
        # Count results
        for result in results:
            total_posts += 1
            if result["success"]:
                successful_posts += 1
    
    logger.info(f"\n🎉 Campaign complete! {successful_posts}/{total_posts} posts successful")
    logger.info(f"📱 Platforms: Instagram, TikTok, Twitter, Facebook, LinkedIn")
    
    return successful_posts, total_posts

def test_single_platform_post():
    """Test posting to a single platform"""
    logger.info("🧪 Testing single platform post...")
    
    generator = MultiPlatformContentGenerator()
    artist = generator.create_artist_profile("test_artist", "Test Artist", "pop", "energetic")
    
    # Test Instagram post
    content = generator.generate_platform_content("instagram", "new-release", "my debut single", artist)
    
    print(f"\n--- Test Instagram Post ---")
    print(f"Artist: {artist['stage_name']}")
    print(f"Caption: {content['caption']}")
    print(f"Hashtags: {' '.join(['#' + tag for tag in content['hashtags']])}")
    print(f"Character count: {content['character_count']}")
    
    return content

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_single_platform_post()
    else:
        run_daily_multi_platform_campaign()
